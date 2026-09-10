"""Capability-limited external memory and evidence gate for the Pi agent.

Only this host can admit facts. All paths are immutable package snapshot IDs. Tools
cannot execute samples, access the network, read arbitrary files, or change rules.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass

from ..facts.model import FactSet
from ..facts.package import SkillPackage
from .state import working_set
from .tools import SnapshotTools


@dataclass(frozen=True)
class Budget:
    max_calls: int = 20
    max_total_tokens: int | None = None
    max_output_tokens: int = 768
    max_context_bytes: int = 14000
    max_context_tokens: int = 16000
    max_tool_calls: int = 80
    max_read_bytes: int | None = None
    max_facts: int = 64
    timeout_seconds: int = 120

    def __post_init__(self) -> None:
        for key, val in asdict(self).items():
            if key in {"max_total_tokens", "max_read_bytes"} and val is None:
                continue
            if type(val) is not int or val <= 0:
                raise ValueError(f"{key} must be a positive integer")
        if self.max_context_tokens > 16000:
            raise ValueError("v3 context token ceiling is 16000")


class AgentHost(SnapshotTools):
    def __init__(
        self,
        package: SkillPackage,
        facts: FactSet,
        budget: Budget | None = None,
        event_sink: Callable[[dict], None] | None = None,
        protocol_version: int = 4,
    ):
        budget = budget or Budget()
        self.protocol_version = protocol_version
        self.reviewed: dict[str, str] = {}
        self.package, self.facts, self.budget = package, facts, budget
        self.files = {f"f{i}": f for i, f in enumerate(package.files)}
        self.reads: dict[str, tuple[str, int, str]] = {}
        self.records: dict[str, object] = {}
        self.notes = ""
        self.events: list[dict] = []
        self.event_sink = event_sink
        self.calls = self.tokens = self.tool_calls = self.read_bytes = self.added = 0
        self.pending = 0
        self.status = "running"
        self.started = time.monotonic()
        self.decisions: dict[tuple[str, str], bool] = {}
        self.event(
            "snapshot",
            schema_version=protocol_version,
            skill=package.name,
            files=[
                {
                    "id": fid,
                    "path": f.path,
                    "size": f.size,
                    "sha256": hashlib.sha256((f.text or "").encode()).hexdigest(),
                }
                for fid, f in self.files.items()
            ],
            budget=asdict(budget),
        )

    def event(self, kind: str, **data) -> None:
        event = {"kind": kind, **data}
        self.events.append(event)
        if self.event_sink:
            self.event_sink(event)

    def check(self) -> None:
        if self.status != "running":
            raise ValueError(f"run stopped: {self.status}")
        if time.monotonic() - self.started >= self.budget.timeout_seconds:
            self.status = "timeout"
            raise ValueError("wall time exhausted")

    def reserve(self, payload_bytes: int, digest: str) -> dict:
        self.check()
        # UTF-8 wire bytes + protocol margin is deliberately conservative, NOT a
        # tokenizer or a billing guarantee. Charge reservation if usage is missing.
        reservation = payload_bytes + 512 + self.budget.max_output_tokens
        if (
            self.pending
            or self.calls >= self.budget.max_calls
            or payload_bytes > self.budget.max_context_bytes
            or reservation > self.budget.max_context_tokens
            or (
                self.budget.max_total_tokens is not None
                and self.tokens + reservation > self.budget.max_total_tokens
            )
        ):
            self.status = "budget_exhausted"
            self.event(
                "request_rejected",
                payload_bytes=payload_bytes,
                reservation=reservation,
                calls=self.calls,
            )
            raise ValueError("model request budget exhausted before dispatch")
        self.calls += 1
        self.pending = reservation
        self.event(
            "request",
            call=self.calls,
            payload_bytes=payload_bytes,
            sha256=digest,
            reserved_tokens=reservation,
        )
        return {"ok": True}

    def usage(self, usage: dict, stop_reason: str) -> dict:
        components = [usage.get(k) for k in ("input", "output", "cacheRead", "cacheWrite")]
        valid = all(type(n) in (int, float) and n >= 0 for n in components)
        total = int(sum(components)) if valid else 0
        self.tokens += total if total > 0 else self.pending
        self.pending = 0
        self.event("usage", usage=usage, accounted_tokens=self.tokens, stop_reason=stop_reason)
        if self.status != "running":
            return {"stop": True}
        if stop_reason in {"error", "aborted", "length"}:
            self.status = "provider_error" if stop_reason == "error" else "incomplete"
        elif not total:
            self.status = "usage_unknown"
        elif (
            self.budget.max_total_tokens is not None and self.tokens >= self.budget.max_total_tokens
        ):
            self.status = "budget_exhausted"
        elif total > self.budget.max_context_tokens:
            self.status = "context_overrun"
        return {"stop": self.status != "running"}

    def context(self) -> dict:
        covered = self.report()["coverage"]
        all_read = all(c["read_bytes"] == c["total_bytes"] for c in covered.values())
        pending_edges = sum(pair not in self.decisions for pair in self.candidates())
        return {
            "files": len(self.files),
            "static_and_admitted_facts": len(self.facts),
            "remaining_calls": self.budget.max_calls - self.calls,
            "remaining_tokens": (
                None
                if self.budget.max_total_tokens is None
                else self.budget.max_total_tokens - self.tokens
            ),
            "remaining_read_bytes": (
                None
                if self.budget.max_read_bytes is None
                else self.budget.max_read_bytes - self.read_bytes
            ),
            "notes": self.notes,
            "latest_records": list(self.records)[-6:],
            "read_handles": len(self.reads),
            "reviewed_edges": len(self.decisions),
            "admitted_observations_and_edges": self.added,
            "pending_edge_count": pending_edges,
            "next_action": "finish" if all_read and not pending_edges else "review",
            "unread_files": sum(
                not any(r[0] == fid for r in self.reads.values()) for fid in self.files
            ),
            "status": self.status,
            "working_set": working_set(self),
        }

    def execute(self, action: str, args: dict) -> dict:
        self.check()
        if self.tool_calls >= self.budget.max_tool_calls:
            self.status = "budget_exhausted"
            raise ValueError("tool call budget exhausted")
        self.tool_calls += 1
        self.event("tool_request", action=action, args=args)
        methods = {
            name: getattr(self, "_" + name)
            for name in (
                "files",
                "read",
                "search",
                "facts",
                "gaps",
                "remember",
                "review",
                "recall",
                "observe",
                "edge",
                "finish",
            )
        }
        try:
            if action not in methods or not isinstance(args, dict):
                raise ValueError("unknown action or invalid arguments")
            result = methods[action](**args)
            if len(json.dumps(result, ensure_ascii=False).encode()) > 6000:
                raise ValueError("tool output too large; request a smaller page")
        except (TypeError, ValueError, KeyError) as exc:
            result = {"error": str(exc)[:300]}
        rid = f"r{self.tool_calls}"
        self.records[rid] = result
        self.event("tool_result", record=rid, result=result)
        return {"record": rid, "data": result, "stop": self.status != "running"}

    def report(self) -> dict:
        coverage = {}
        for fid, f in self.files.items():
            ranges = sorted(
                (start, start + len(text.encode()))
                for file, start, text in self.reads.values()
                if file == fid
            )
            end = covered = 0
            for a, b in ranges:
                covered += max(0, b - max(end, a))
                end = max(end, b)
            coverage[fid] = {"path": f.path, "read_bytes": covered, "total_bytes": f.size}
        complete = (
            self.status == "completed"
            and not self.package.issues
            and all(c["read_bytes"] == c["total_bytes"] for c in coverage.values())
        )
        return {
            "status": self.status,
            "coverage_complete": complete,
            "coverage": coverage,
            "calls": self.calls,
            "accounted_tokens": self.tokens + self.pending,
            "tool_calls": self.tool_calls,
            "read_bytes": self.read_bytes,
            "observations_and_edges": self.added,
            "load_issues": self.package.issues,
        }
