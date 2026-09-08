"""A small rule language that compiles to engine rules.

The point of a DSL here is that adding a detection should be writing a rule, not editing
the engine — and that the rule reads like the claim it encodes, so an analyst can review it
and a reviewer can argue with it. It is honest Datalog with one piece of sugar: a `rule`
block that attaches the metadata an alert needs to describe itself.

Conventions, chosen to match standard Datalog so the syntax is not a surprise:

    Capitalized names are variables      A, Chunk, File2
    snake_case names are predicates       targets_sensitive, mentions_external_host
    _ (or _name) is a don't-care variable, fresh at each occurrence
    "quoted" or bare-lowercase tokens are constants

Predicates map to engine fact predicates by PascalCasing:
    targets_sensitive  -> TargetsSensitive        includes -> Includes

Two statement forms:

    # a library clause (transitive closure, bridging lemmas) ends with a period
    reaches(C1, C2) :- in_file(C1, F1), includes(F1, F2), in_file(C2, F2).

    # an alert rule block carries severity / emitted pattern / message
    rule exfil_chain severity=HIGH emits=E1 min_confidence=0.4 {
        targets_sensitive(C)
        reaches(C, E)
        egress(E)
        => "credential read reaches an external egress"
    }
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..engine.datalog import Atom, BodyItem, Compare, Neg, Rule, Term, Var

_COMMENT = re.compile(r"(?m)(#|//).*$")
_BLOCK = re.compile(r"rule\s+([A-Za-z_]\w*)\s*([^\{]*)\{(.*?)\}", re.S)
_ATOM = re.compile(r"([a-z_]\w*)\s*\(([^)]*)\)")
_COMPARE = re.compile(r"^\s*([A-Za-z_]\w*)\s*(==|!=)\s*([A-Za-z_\"'][\w\"']*)\s*$")
_HEADER_KV = re.compile(r"(\w+)\s*=\s*([^\s]+)")


class DslError(ValueError):
    """A rule file could not be parsed."""


@dataclass(frozen=True)
class _Anon:
    """A counter handing out fresh names for each `_` so occurrences do not unify."""

    def __init__(self) -> None:
        object.__setattr__(self, "_n", [0])

    def next(self) -> str:
        self._n[0] += 1  # type: ignore[attr-defined]
        return f"_anon{self._n[0]}"  # type: ignore[attr-defined]


def compile_rules(text: str) -> list[Rule]:
    """Compile DSL source into engine rules (library clauses first, then alert blocks)."""
    text = _COMMENT.sub("", text)
    rules: list[Rule] = []

    blocks = list(_BLOCK.finditer(text))
    remainder = _BLOCK.sub("", text)

    for clause in _split_clauses(remainder):
        rules.append(_parse_clause(clause))

    for m in blocks:
        rules.append(_parse_block(m.group(1), m.group(2), m.group(3)))

    return rules


def _split_clauses(text: str) -> list[str]:
    return [c.strip() for c in text.split(".") if c.strip()]


def _parse_clause(clause: str) -> Rule:
    if ":-" not in clause:
        raise DslError(f"library clause needs ':-': {clause!r}")
    head_src, body_src = clause.split(":-", 1)
    anon = _Anon()
    head = _parse_atom(head_src.strip(), anon)
    body = _parse_body(body_src, anon)
    return Rule(head=head, body=body, name=head.predicate.lower())


def _parse_block(name: str, header: str, body_src: str) -> Rule:
    meta = dict(_HEADER_KV.findall(header))
    message = ""
    lines: list[str] = []
    for raw in body_src.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("=>"):
            message = line[2:].strip().strip("\"'")
        else:
            lines.append(line)
    anon = _Anon()
    body = _parse_body(",".join(lines), anon)
    return Rule(
        head=Atom("Alert", (name,)),
        body=body,
        name=name,
        severity=meta.get("severity", "MEDIUM").upper(),
        emits=meta.get("emits", ""),
        message=message,
        min_confidence=float(meta.get("min_confidence", 0.0)),
    )


def _parse_body(src: str, anon: _Anon) -> tuple[BodyItem, ...]:
    items: list[BodyItem] = []
    for piece in _split_body(src):
        piece = piece.strip()
        if not piece:
            continue
        if cmp := _COMPARE.match(piece):
            left, op, right = cmp.groups()
            items.append(
                Compare("eq" if op == "==" else "neq", _term(left, anon), _term(right, anon))
            )
        elif piece.startswith("not "):
            items.append(Neg(_parse_atom(piece[4:].strip(), anon)))
        else:
            items.append(_parse_atom(piece, anon))
    return tuple(items)


def _split_body(src: str) -> list[str]:
    """Split a body on commas that are not inside parentheses."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(src):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(src[start:i])
            start = i + 1
    out.append(src[start:])
    return out


def _parse_atom(src: str, anon: _Anon) -> Atom:
    m = _ATOM.fullmatch(src.strip())
    if not m:
        raise DslError(f"not an atom: {src!r}")
    predicate = _pascal(m.group(1))
    args = tuple(_term(a.strip(), anon) for a in m.group(2).split(",") if a.strip())
    return Atom(predicate, args)


def _term(token: str, anon: _Anon) -> Term:
    if token in ("_", ""):
        return Var(anon.next())
    if token.startswith("_"):
        return Var(token)
    if token[0].isupper():
        return Var(token)
    return token.strip("\"'")


def _pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))
