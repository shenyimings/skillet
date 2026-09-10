"""Deterministic, bounded working state survives conversation eviction.

The model does not have to remember to write a scratchpad to keep source handles or
pending edge IDs. Source excerpts enter this state only after an explicit source read.
"""

import json


def working_set(host) -> dict:
    state = {"files": [], "facts": [], "pending_edges": [], "evidence": []}

    def append(group, row):
        state[group].append(row)
        if len(json.dumps(state, ensure_ascii=False).encode()) > 3600:
            state[group].pop()
            return False
        return True

    for fid, file in list(host.files.items())[:5]:
        handles = [
            {"source": h, "start": start, "end": start + len(text.encode())}
            for h, (f, start, text) in host.reads.items()
            if f == fid
        ]
        row = {"id": fid, "path": file.path[:120], "bytes": file.size, "read_sources": handles[-2:]}
        if file.language_hint not in {"markdown", "yaml", "json", "toml"}:
            row["required_gap"] = f"code:{fid}"
        append("files", row)

    # Preserve source handles and exact short excerpts without reloading any file.
    # Reserve room for the frontier; long excerpts remain available via read/recall.
    for handle, (fid, start, text) in list(host.reads.items())[-4:]:
        excerpt = text.encode()[:400].decode(errors="ignore")
        append(
            "evidence",
            {
                "source": handle,
                "file": fid,
                "start": start,
                "text": excerpt,
                "truncated": excerpt != text,
            },
        )

    for a, b in host.candidates():
        if (a, b) not in host.decisions:
            if not append("pending_edges", {"source_locus": a, "target_locus": b}):
                break
            if len(state["pending_edges"]) >= 4:
                break

    for predicate in (
        "StrongSecret",
        "Net",
        "Claim",
        "Read",
        "Exec",
        "Write",
        "ConfirmedFlow",
        "RejectedFlow",
        "Obfuscation",
    ):
        for fact in host.facts.match(predicate):
            if not append(
                "facts", {"predicate": fact.predicate, "args": fact.args, "origin": fact.origin}
            ):
                break
            if len(state["facts"]) >= 8:
                break
        if len(state["facts"]) >= 8:
            break
    state["note"] = "Bounded working set, not exhaustive. Use paged tools for omitted entries."
    return state
