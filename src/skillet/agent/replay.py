"""Offline replay of evidence decisions, usage and external state. Never calls Pi/API."""

from __future__ import annotations

import json
from pathlib import Path

from ..facts.package import SkillPackage
from .host import AgentHost, Budget
from .static import static_facts


def replay(path: Path, package: SkillPackage) -> AgentHost:
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not events or events[0].get("kind") != "snapshot":
        raise ValueError("audit is missing its initial snapshot")
    version = events[0].get("schema_version", 3)
    if version not in {3, 4}:
        raise ValueError("unsupported audit schema version")
    host = AgentHost(
        package,
        static_facts(package, legacy=version == 3),
        Budget(**events[0]["budget"]),
        protocol_version=version,
    )
    if host.events[0] != events[0]:
        raise ValueError("source snapshot changed; replay refused")
    last_result = None
    for event in events[1:]:
        kind = event["kind"]
        if kind == "request":
            host.reserve(event["payload_bytes"], event["sha256"])
        elif kind == "usage":
            host.usage(event["usage"], event["stop_reason"])
        elif kind == "tool_request":
            last_result = host.execute(event["action"], event["args"])
        elif kind == "tool_result":
            # JSON normalizes tuples to arrays; compare canonical serialized values.
            if last_result is None or json.dumps(last_result["data"], sort_keys=True) != json.dumps(
                event["result"], sort_keys=True
            ):
                raise ValueError("tool replay diverged from audit")
        elif kind == "report":
            host.status = event["status"]
        elif kind == "resume":
            host.status = "running"
    if host.status == "running":
        host.status = "interrupted"
    return host
