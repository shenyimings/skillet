"""The v2 fact vocabulary: a small capability / information-flow calculus.

v1's predicates named attacks (`MentionsSensitivePath`, `NetworkSink`); anything outside
the enumerated tables produced no fact and no rule could fire. v2 names *primitives* —
verbs over a small resource lattice, joined by information flow — so a novel resource or a
novel channel is still expressible in the existing vocabulary. Both the static extractors
and the LLM labeller populate these same names; rules compose them.

This module is only definitions and small builders, so extractors and rules share one
canonical spelling. See docs/v2-design.md for the rationale.
"""

from __future__ import annotations

from enum import StrEnum


class Pred(StrEnum):
    """Every predicate a fact may use. Rules and extractors reference these, not literals."""

    # verbs
    READ = "Read"  # Read(loc, class)
    WRITE = "Write"  # Write(loc, class)
    EXEC = "Exec"  # Exec(loc)
    NET = "Net"  # Net(loc, direction)
    FLOW = "Flow"  # Flow(a, b) — derived, but the LLM may assert it too
    DIRECTIVE = "Directive"  # Directive(loc)
    CLAIM = "Claim"  # Claim(loc, kind)
    DECLARES = "Declares"  # Declares(skill, capability)
    STRONG_SECRET = "StrongSecret"  # StrongSecret(loc) — a credential file / harvest / OOD secret
    PIPE_TO_SHELL = "PipeToShell"  # PipeToShell(loc) — curl|sh fetch-and-run at one locus
    # evidence / attributes
    ENDPOINT = "Endpoint"  # Endpoint(loc, host)
    OBFUSCATION = "Obfuscation"  # Obfuscation(loc, kind)
    ATTR = "Attr"  # Attr(loc, key, value)
    COINSKILL = "CoInSkill"  # CoInSkill(a, b) — weak same-package reachability
    # structural
    INFILE = "InFile"  # InFile(loc, file)
    INCLUDES = "Includes"  # Includes(file, file)
    FILE = "File"  # File(skill, file, language)


class Resource(StrEnum):
    """The resource lattice. Few and categorical, so an OOD resource still lands somewhere."""

    SECRET = "secret"  # credentials, keys, tokens, passwords, cloud metadata
    PERSONAL = "personal"  # user PII, conversation/context, browser data
    AGENT_STATE = "agent_state"  # CLAUDE.md, .claude/, agent memory/config
    CODE = "code"  # scripts, dependencies, interpreter input
    SYSTEM = "system"  # environment variables, arbitrary/system files, process state


class Direction(StrEnum):
    OUT = "out"  # data leaves the environment (any channel)
    IN = "in"  # data / code enters (a fetch)
    UNKNOWN = "unknown"


class Claim(StrEnum):
    """Framing claims — the social/injection layer, not information flow."""

    AUTHORITY = "authority"  # asserts control over the agent / precedence over the user
    CONCEAL = "conceal"  # asks to hide or not mention something to the user
    PERSIST = "persist"  # declares itself standing/binding beyond the task
    DECEIVE = "deceive"  # misrepresents what it does


class Obfuscation(StrEnum):
    CONFUSABLE = "confusable"
    ZERO_WIDTH = "zero_width"
    PADDING = "padding"
    OVERSIZE = "oversize"
    ENCODED = "encoded"  # a decoded blob wired to an execution sink


class Capability(StrEnum):
    """Frontmatter-declared grants (the declared side of over-privilege)."""

    WILDCARD = "wildcard"  # e.g. Bash(*)
    UNATTENDED = "unattended"  # bypassPermissions / acceptEdits / dontAsk


# Resource classes a rule treats as sensitive to read (the exfil source set).
SENSITIVE_READ = frozenset({Resource.SECRET, Resource.PERSONAL})

__all__ = [
    "SENSITIVE_READ",
    "Capability",
    "Claim",
    "Direction",
    "Obfuscation",
    "Pred",
    "Resource",
]
