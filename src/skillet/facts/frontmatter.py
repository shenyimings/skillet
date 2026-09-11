"""Frontmatter facts: what the skill declares about itself.

The declaration is half of every over-privilege rule — the other half being what the skill
actually does. Parsing is lenient on purpose: a skill whose frontmatter is malformed still
gets analysed, and the malformation is itself recorded, because "unparseable metadata" is
a state worth alerting on rather than a reason to abort.
"""

from __future__ import annotations

import re
from collections.abc import Iterator

import yaml

from .model import Fact, Origin, Span
from .package import SkillPackage

EXTRACTOR = "frontmatter"

_FENCE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)

# Tool grants that hand over broad or unattended capability.
_WILDCARD_TOOL = re.compile(r"\*|\ball\b", re.I)
_UNATTENDED_MODES = frozenset({"bypasspermissions", "acceptedits", "dontask", "auto"})


def extract(package: SkillPackage) -> Iterator[Fact]:
    """Emit declaration facts from the package entrypoint's YAML frontmatter."""
    entry = package.entrypoint
    if entry is None or entry.text is None:
        yield Fact("MissingEntrypoint", (package.name,), extractor=EXTRACTOR)
        return

    match = _FENCE.match(entry.text)
    if match is None:
        yield Fact(
            "NoFrontmatter",
            (package.name,),
            extractor=EXTRACTOR,
            span=Span(entry.path, 0, 0, 1),
        )
        return

    span = Span.locate(entry.path, entry.text, match.start(1), match.end(1))

    def fact(predicate: str, *args: str, confidence: float = 1.0) -> Fact:
        return Fact(
            predicate=predicate,
            args=args,
            origin=Origin.STATIC,
            confidence=confidence,
            span=span,
            extractor=EXTRACTOR,
        )

    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        yield fact("MalformedFrontmatter", package.name)
        return
    if not isinstance(meta, dict):
        yield fact("MalformedFrontmatter", package.name)
        return

    if not meta.get("description"):
        yield fact("Declares", package.name, "no_description")

    # Declared capability grants — the "declared" half of over-privilege. Kept general:
    # each tool is a Declares(skill, <tool>), with wildcard / unattended flagged as such.
    for tool in _tools(meta):
        yield fact("Declares", package.name, tool.lower())
        if _WILDCARD_TOOL.search(tool):
            yield fact("Declares", package.name, "wildcard")

    mode = meta.get("permissionMode") or meta.get("permission_mode")
    if mode and str(mode).replace("-", "").replace("_", "").lower() in _UNATTENDED_MODES:
        yield fact("Declares", package.name, "unattended")


def _tools(meta: dict) -> Iterator[str]:
    """Tool grants, from whichever of the competing frontmatter spellings is present."""
    for key in ("allowed-tools", "allowed_tools", "allowedTools", "tools"):
        value = meta.get(key)
        if value is None:
            continue
        if isinstance(value, str):
            yield from (t.strip() for t in value.split(",") if t.strip())
        else:
            yield from _sequence(value)


def _sequence(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, (list, tuple)):
        yield from (str(v) for v in value)


def _stringify(value: object) -> str:
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    return str(value)
