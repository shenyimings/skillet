"""Snapshot capabilities. State lives in AgentHost; no arbitrary filesystem or execution."""

from __future__ import annotations

import json
from dataclasses import asdict

from ..facts.model import Fact, Origin, Span
from ..llm.schema import Label
from .static import locus

LABELS = {
    "reads_sensitive": ("Read", "secret"),
    "reads_personal": ("Read", "personal"),
    "sends_outward": ("Net", "out"),
    "fetches_remote": ("Net", "in"),
    "executes_code": ("Exec",),
    "writes_agent_state": ("Write", "agent_state"),
    "overrides_constraints": ("Claim", "override"),
    "claims_authority": ("Claim", "authority"),
    "asks_to_conceal": ("Claim", "conceal"),
    "claims_persistent": ("Claim", "persist"),
    "misrepresents": ("Claim", "deceive"),
    "instructs_agent": ("Directive",),
}


class SnapshotTools:
    def _bounded_text(self, text: str) -> str:
        # Keep evidence actually visible in the next model turn, including JSON escaping.
        # Oversized source results must not be counted as read and then context-truncated.
        if self.protocol_version >= 4:
            low, high = 0, len(text)
            while low < high:
                mid = (low + high + 1) // 2
                if len(json.dumps(text[:mid], ensure_ascii=False).encode()) <= 1100:
                    low = mid
                else:
                    high = mid - 1
            return text[:low]
        while len(json.dumps(text, ensure_ascii=False).encode()) > 1100:
            text = text[: len(text) // 2]
        return text

    @staticmethod
    def _page(items: list, offset: int = 0) -> dict:
        if type(offset) is not int or offset < 0:
            raise ValueError("offset must be a nonnegative integer")
        page = items[offset : offset + 5]
        return {"items": page, "next": offset + 5 if offset + 5 < len(items) else None}

    def _files(self, offset: int = 0) -> dict:
        return self._page(
            [
                {
                    "id": fid,
                    "path": f.path[:200],
                    "bytes": f.size,
                    "language": f.language_hint,
                    "text": f.scannable,
                    "truncated": f.oversized,
                    **(self.read_state(fid) if self.protocol_version >= 4 else {}),
                }
                for fid, f in self.files.items()
            ],
            offset,
        )

    def read_state(self, file: str) -> dict:
        ranges = sorted(
            (start, start + len(text.encode()))
            for fid, start, text in self.reads.values()
            if fid == file
        )
        merged = []
        for a, b in ranges:
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(b, merged[-1][1])
            else:
                merged.append([a, b])
        cursor = merged[0][1] if merged and merged[0][0] == 0 else 0
        return {
            "read_ranges": merged[:8],
            "ranges_truncated": len(merged) > 8,
            "next_unread": cursor if cursor < self.files[file].size else None,
            "reviewed": file in self.reviewed,
        }

    def _review(self, file: str, reason: str) -> dict:
        if not isinstance(reason, str) or not 1 <= len(reason) <= 300:
            raise ValueError("review reason must have 1..300 characters")
        if self.read_state(file)["next_unread"] is not None:
            raise ValueError("file has unread bytes; finish may explicitly leave partial coverage")
        self.reviewed[file] = reason
        return {"reviewed": file, "reason": reason}

    def _read(self, file: str, start: int | None = None, size: int = 1800, gap: str = "") -> dict:
        if start is None:
            start = self.read_state(file)["next_unread"] if self.protocol_version >= 4 else 0
            if start is None:
                return {
                    "already_read": True,
                    "file": file,
                    "next": None,
                    "instruction": "Review existing evidence, submit if needed, then finish. "
                    "Use an explicit byte start only to revisit evidence.",
                }
        f = self.files[file]
        if type(start) is not int or type(size) is not int or start < 0 or not 1 <= size <= 2400:
            raise ValueError("read uses UTF-8 byte offsets, size 1..2400")
        if f.text is None:
            raise ValueError("binary/unreadable file")
        if f.language_hint not in {"markdown", "yaml", "json", "toml"} and gap != f"code:{file}":
            raise ValueError(f"code reads require unresolved static-review gap code:{file}")
        raw = f.text.encode()
        if start >= len(raw) and raw:
            raise ValueError("start beyond source")
        # Require an exact UTF-8 start; trim an incomplete final character only.
        raw[:start].decode()
        text = self._bounded_text(raw[start : start + size].decode(errors="ignore"))
        count = len(text.encode())
        if not count and start < len(raw):
            raise ValueError("window ends inside a UTF-8 character; increase size")
        if self.protocol_version >= 4:
            for handle, existing in self.reads.items():
                if existing == (file, start, text):
                    return {
                        "source": handle,
                        "start": start,
                        "end": start + count,
                        "text": text,
                        "next": start + count if start + count < len(raw) else None,
                        "cached": True,
                    }
        if (
            self.budget.max_read_bytes is not None
            and self.read_bytes + count > self.budget.max_read_bytes
        ):
            self.status = "budget_exhausted"
            raise ValueError("source read budget exhausted")
        self.read_bytes += count
        handle = f"s{len(self.reads)}"
        self.reads[handle] = (file, start, text)
        return {
            "source": handle,
            "start": start,
            "end": start + count,
            "text": text,
            "next": start + count if start + count < len(raw) else None,
        }

    def _search(self, text: str, file: str, start: int = 0, gap: str = "") -> dict:
        if not isinstance(text, str) or not 1 <= len(text) <= 120:
            raise ValueError("literal query length 1..120")
        if type(start) is not int or start < 0:
            raise ValueError("start must be a nonnegative byte offset")
        f = self.files[file]
        if f.language_hint not in {"markdown", "yaml", "json", "toml"} and gap != f"code:{file}":
            raise ValueError(f"code searches require unresolved static-review gap code:{file}")
        raw = (f.text or "").encode()
        pos = raw.find(text.encode(), start)
        if pos < 0:
            return {"found": False}
        # Search excerpts use the exact same code gate and read accounting as reads.
        result = self._read(file, pos, 1000, gap)
        return {"found": True, **result}

    def _facts(self, predicate: str = "", offset: int = 0) -> dict:
        facts = self.facts.match(predicate) if predicate else list(self.facts)
        if not predicate and self.protocol_version >= 4:
            facts.sort(
                key=lambda f: (
                    f.predicate in {"File", "InFile", "NoFrontmatter", "Skill"},
                    f.predicate,
                    f.args,
                )
            )
        return self._page(
            [
                {
                    "predicate": f.predicate,
                    "args": f.args,
                    "origin": f.origin,
                    "span": asdict(f.span) if f.span else None,
                }
                for f in facts
            ],
            offset,
        )

    def candidates(self) -> list[tuple[str, str]]:
        sources = {f.args[0] for p in ("Read", "StrongSecret") for f in self.facts.match(p)}
        sinks = {f.args[0] for f in self.facts.match("Net") if f.args[1] == "out"}
        authority = {f.args[0] for f in self.facts.match("Claim") if f.args[1] == "authority"}
        conceal = {f.args[0] for f in self.facts.match("Claim") if f.args[1] == "conceal"}
        encoded = {f.args[0] for f in self.facts.match("Obfuscation") if f.args[1] == "encoded"}
        sockets = {
            f.args[0] for f in self.facts.match("Attr") if f.args[1:] == ("channel", "socket")
        }
        execution = {f.args[0] for f in self.facts.match("Exec")}
        pairs = []
        for left, right in (
            (sources, sinks),
            (authority, conceal),
            (encoded, execution),
            (sockets, execution),
        ):
            for a in sorted(left):
                for b in sorted(right):
                    if a != b and ("ConfirmedFlow", (a, b)) not in self.facts:
                        pairs.append((a, b))
                        if len(pairs) >= 128:
                            return pairs
        return pairs

    def _gaps(self, offset: int = 0) -> dict:
        gaps = [
            {
                "id": f"code:{fid}",
                "file": fid,
                "reason": "static analysis is partial; inspect only to resolve a fact or edge",
            }
            for fid, f in self.files.items()
            if f.scannable
            and f.language_hint not in {"markdown", "yaml", "json", "toml"}
            and (self.protocol_version < 4 or fid not in self.reviewed)
        ]
        gaps.extend(
            {"source": a, "target": b, "reason": "co-presence is not flow"}
            for a, b in self.candidates()
            if (a, b) not in self.decisions
        )
        return self._page(gaps, offset)

    def _remember(self, text: str) -> dict:
        if not isinstance(text, str) or len(text.encode()) > 1000:
            raise ValueError("notes must fit 1000 UTF-8 bytes")
        self.notes = text
        return {"saved": True}

    def _recall(self, record: str, start: int = 0, size: int = 1000) -> object:
        if type(start) is not int or start < 0 or type(size) is not int or not 1 <= size <= 1000:
            raise ValueError("recall character range: start>=0, size=1..1000")
        text = json.dumps(self.records[record], ensure_ascii=False)
        fragment = self._bounded_text(text[start : start + size])
        return {
            "record": record,
            "text": fragment,
            "next": start + len(fragment) if start + len(fragment) < len(text) else None,
        }

    def _anchor(self, source: str, quote: str, offset: int | None = None) -> Span:
        fid, start, text = self.reads[source]
        if offset is None:
            offset = text.find(quote)
            if offset < 0 or text.find(quote, offset + 1) >= 0:
                raise ValueError("quote must occur exactly once, or supply its character offset")
        if type(offset) is not int or offset < 0 or not quote:
            raise ValueError("quote and nonnegative character offset required")
        if text[offset : offset + len(quote)] != quote:
            raise ValueError("quote does not match previously read source at offset")
        byte_start = start + len(text[:offset].encode())
        file = self.files[fid]
        line = (file.text or "").encode()[:byte_start].count(b"\n") + 1
        return Span(file.path, byte_start, byte_start + len(quote.encode()), line)

    def _observe(
        self, source: str, label: dict, offset: int | None = None, support: dict | None = None
    ) -> dict:
        item = Label.model_validate(label)
        span = self._anchor(source, item.quote, offset)
        contrary = None
        if self.protocol_version >= 5 and item.observation == "misrepresents":
            if not isinstance(support, dict):
                raise ValueError(
                    "misrepresents needs support: source, quote, optional offset "
                    "for contradictory actual behavior"
                )
            if support.get("quote") == item.quote:
                raise ValueError("claim and contradictory behavior cannot be the same quote")
            contrary = self._anchor(**support)
            if contrary.file == span.file and not (
                contrary.end <= span.start or span.end <= contrary.start
            ):
                raise ValueError(
                    "reported claim and actual behavior need distinct, non-overlapping evidence"
                )
        if (
            self.protocol_version >= 4
            and (LABELS[item.observation][0], (locus(span), *LABELS[item.observation][1:]))
            in self.facts
        ):
            return {"locus": locus(span), "accepted": True, "already_present": True}
        if self.added >= self.budget.max_facts:
            self.status = "budget_exhausted"
            raise ValueError("observation/edge budget exhausted")
        node = locus(span)
        pred, *args = LABELS[item.observation]
        facts = [(pred, (node, *args)), ("InFile", (node, span.file))]
        if item.observation in {"reads_sensitive", "reads_personal"}:
            facts.append(("StrongSecret", (node,)))
        for predicate, arguments in facts:
            self.facts.add(
                Fact(predicate, arguments, Origin.LLM, item.confidence, span, "pi-agent")
            )
        if contrary is not None:
            self.facts.add(
                Fact(
                    "DeceptionEvidence",
                    (node, locus(contrary)),
                    Origin.LLM,
                    item.confidence,
                    contrary,
                    "pi-agent-contrast",
                )
            )
        self.added += 1
        self.event("admitted", observation=item.model_dump(), span=asdict(span), locus=node)
        return {"locus": node, "accepted": True}

    def _edge(
        self,
        source_locus: str,
        target_locus: str,
        confirmed: bool,
        source: str,
        quote: str,
        reason: str,
        offset: int | None = None,
    ) -> dict:
        if (
            type(confirmed) is not bool
            or not isinstance(reason, str)
            or not 1 <= len(reason) <= 300
        ):
            raise ValueError("edge requires boolean confirmed and reason of 1..300 characters")
        if len(quote) > 600:
            raise ValueError("edge quote too long")
        pair = (source_locus, target_locus)
        if self.protocol_version >= 4 and pair in self.decisions:
            if self.decisions[pair] != confirmed:
                raise ValueError("edge already decided with a different value")
            return {"accepted": True, "already_decided": True}
        # Endpoint membership does not depend on the capped candidate suggestion list.
        nodes = {f.args[0] for f in self.facts.match("InFile")}
        if source_locus not in nodes or target_locus not in nodes or pair in self.decisions:
            raise ValueError("unknown endpoints or edge already decided")
        if ("ConfirmedFlow", pair) in self.facts:
            raise ValueError("cannot override a static confirmed edge")
        for endpoint in pair:
            spans = [
                f.span
                for f in self.facts.match("InFile")
                if f.args[0] == endpoint and f.span is not None
            ]
            if not any(
                self.files[fid].path == s.file
                and start <= s.start
                and start + len(text.encode()) >= s.end
                for s in spans
                for fid, start, text in self.reads.values()
            ):
                raise ValueError("read both endpoint spans before deciding an edge")
        span = self._anchor(source, quote, offset)
        if self.added >= self.budget.max_facts:
            self.status = "budget_exhausted"
            raise ValueError("observation/edge budget exhausted")
        self.decisions[pair] = confirmed
        self.added += 1
        pred = "ConfirmedFlow" if confirmed else "RejectedFlow"
        self.facts.add(Fact(pred, pair, Origin.LLM, 0.7, span, "pi-agent-edge"))
        self.event(
            "edge",
            source=source_locus,
            target=target_locus,
            confirmed=confirmed,
            reason=reason,
            span=asdict(span),
        )
        return {"accepted": True}

    def _finish(
        self, observations: list | None = None, edges: list | None = None, reason: str = "", **extra
    ) -> dict:
        if self.protocol_version >= 6:
            from .submission import finish_partial

            return finish_partial(self, observations, edges, reason, **extra)
        if extra:
            raise TypeError("unexpected finish arguments")
        if (
            not isinstance(reason, str)
            or len(reason) > 1000
            or any(
                not isinstance(items, list) or len(items) > 6
                for items in (observations or [], edges or [])
            )
        ):
            raise ValueError("finish allows up to 6 observations/edges and a 1000-character reason")
        for item in observations or []:
            self._observe(**item)
        for item in edges or []:
            self._edge(**item)
        self.status = "completed"
        return {"finished": True, "coverage_complete": self.report()["coverage_complete"]}
