"""NDJSON adapter to Pi. No key or provider error text is written to the audit log."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlparse

from ..facts.model import FactSet
from ..facts.package import SkillPackage
from .host import AgentHost, Budget
from .replay import replay

BRIDGE = Path(__file__).parent / "pi" / "bridge.mjs"


class PiAgent:
    def __init__(
        self,
        *,
        budget: Budget | None = None,
        node: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        audit_path: Path | None = None,
        resume_from: Path | None = None,
    ):
        self.budget = budget or Budget()
        self.node = node or os.environ.get("SKILLET_NODE", "node")
        self.model = model or os.environ.get("SKILLET_LLM_MODEL", "deepseek-v4-flash")
        self.base_url = base_url or os.environ.get(
            "SKILLET_LLM_BASE_URL", "https://api.deepseek.com"
        )
        self.audit_path = audit_path or Path(".cache/agent") / f"{uuid.uuid4().hex}.jsonl"
        self.resume_from = resume_from

    def run(self, package: SkillPackage, facts: FactSet) -> dict:
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        # Open before dispatch, so an existing result cannot trigger paid work first.
        with self.audit_path.open("x", encoding="utf-8") as stream:

            def persist(event: dict) -> None:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())

            restored = None
            if self.resume_from is not None:
                restored = replay(self.resume_from, package)
                if restored.budget != self.budget:
                    raise ValueError("resume must preserve the original budget")
                if restored.status == "completed":
                    raise ValueError("completed runs cannot be resumed")
                for line in self.resume_from.read_text().splitlines():
                    persist(json.loads(line))
                facts.extend(e for f in restored.facts for e in restored.facts.evidence(f))
                restored.facts = facts
                restored.event_sink = persist
                if restored.pending:
                    restored.usage({}, "aborted")  # Charge any uncertain prior request.
                restored.status = "running"
                restored.started = time.monotonic()
                restored.event("resume", previous_audit=self.resume_from.name)
            return self._run(package, facts, persist, restored)

    def _run(self, package: SkillPackage, facts: FactSet, persist, restored=None) -> dict:
        host = restored or AgentHost(package, facts, self.budget, event_sink=persist)
        endpoint = urlparse(self.base_url)
        if endpoint.username or endpoint.password or endpoint.query:
            raise ValueError("credentials must be environment variables, not endpoint URLs")
        local = endpoint.hostname in {"localhost", "127.0.0.1", "::1"}
        if endpoint.scheme != "https" and not (local and endpoint.scheme == "http"):
            raise ValueError("provider endpoint must use HTTPS (except loopback tests)")
        key = os.environ.get("SKILLET_LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("Set SKILLET_LLM_API_KEY or DEEPSEEK_API_KEY in the environment")
        if not (BRIDGE.parent / "node_modules").is_dir():
            raise RuntimeError(
                f"Pi dependencies missing; run npm ci --ignore-scripts in {BRIDGE.parent}"
            )
        config = {
            "budget": asdict(self.budget),
            "model": self.model,
            "base_url": self.base_url,
            "disable_thinking": True,
            "resumed": restored is not None,
        }
        host.event("runtime", model=self.model, base_url=self.base_url, pi_version="0.85.1")
        # Never inherit NODE_OPTIONS, plugin loaders, unrelated service keys or telemetry
        # configuration into the analysis runtime.
        env = {"PATH": os.environ.get("PATH", ""), "SKILLET_LLM_API_KEY": key}
        with tempfile.TemporaryFile() as stderr:
            process = subprocess.Popen(
                [self.node, str(BRIDGE)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=stderr,
                text=True,
                env=env,
            )
            timer = threading.Timer(self.budget.timeout_seconds, process.kill)
            timer.start()
            try:
                process.stdin.write(json.dumps({"init": config}) + "\n")
                process.stdin.flush()
                for line in process.stdout:
                    request = json.loads(line)
                    try:
                        result = self._dispatch(host, request["method"], request.get("params", {}))
                        reply = {"id": request["id"], "result": result}
                    except (ValueError, TypeError, KeyError) as exc:
                        reply = {"id": request["id"], "error": str(exc)[:300]}
                    process.stdin.write(json.dumps(reply) + "\n")
                    process.stdin.flush()
                process.wait()
                if host.status == "running":
                    host.status = "incomplete" if process.returncode == 0 else "runtime_error"
            except (OSError, ValueError, KeyError):
                host.status = "runtime_error"
            finally:
                timer.cancel()
                if process.poll() is None:
                    process.kill()
                process.wait()
                process.stdin.close()
                process.stdout.close()
                if process.returncode == -9:
                    host.status = "timeout"
        report = host.report()
        host.event("report", **report)
        return report

    @staticmethod
    def _dispatch(host: AgentHost, method: str, params: dict) -> object:
        if method in {"reserve", "usage", "context"}:
            return getattr(host, method)(**params)
        if method == "tool":
            return host.execute(**params)
        if method in {"context_audit", "message"}:
            host.event(method, **params)
            return {}
        if method in {"done", "failed"}:
            if host.status == "running":
                host.status = "incomplete" if method == "done" else "runtime_error"
            return host.report()
        raise ValueError("unknown bridge method")
