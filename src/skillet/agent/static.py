"""Static-first event facts. Co-location is not dataflow.

The language-independent scanner remains a conservative lexical fallback. Python adds
AST evidence for direct assignments into outbound payload arguments. No sample executes.
This deliberately does not claim interprocedural or multi-language taint completeness.
"""

from __future__ import annotations

import ast
from dataclasses import replace

from ..facts import extract
from ..facts.model import Fact, FactSet, Span
from ..facts.package import SkillPackage

_EVENTS = {
    "Read",
    "Write",
    "Exec",
    "Net",
    "StrongSecret",
    "Claim",
    "Directive",
    "PipeToShell",
    "Endpoint",
    "Obfuscation",
    "Attr",
}


def locus(span: Span) -> str:
    return f"{span.file}@{span.start}:{span.end}"


def static_facts(package: SkillPackage) -> FactSet:
    """Split legacy file-wide primitives into anchored events, then add AST flow."""
    result = extract(package)
    out = FactSet()
    for fact in result:
        for evidence in result.evidence(fact):
            span = evidence.span
            if evidence.predicate in _EVENTS and span is not None:
                node = locus(span)
                out.add(replace(evidence, args=(node, *evidence.args[1:])))
                out.add(Fact("InFile", (node, span.file), span=span, extractor="v3-locus"))
            else:
                out.add(evidence)
    for file in package.scannable():
        if file.language_hint == "python":
            out.extend(_python(file.path, file.text or ""))
    return out


def _python(path: str, text: str) -> list[Fact]:
    try:
        tree = ast.parse(text)
    except (SyntaxError, RecursionError, ValueError):
        return []  # The host exposes a code-review gap; lexical facts remain.
    raw_lines = text.encode("utf-8").splitlines(keepends=True)
    starts = [0]
    for line in raw_lines:
        starts.append(starts[-1] + len(line))
    facts: list[Fact] = []

    def span(node: ast.AST) -> Span:
        return Span(
            path,
            starts[node.lineno - 1] + node.col_offset,
            starts[node.end_lineno - 1] + node.end_col_offset,
            node.lineno,
        )

    def emit(pred: str, node: ast.AST, *args: str) -> str:
        loc = span(node)
        ident = locus(loc)
        facts.append(Fact(pred, (ident, *args), span=loc, extractor="python-ast"))
        facts.append(Fact("InFile", (ident, path), span=loc, extractor="python-ast"))
        return ident

    def name(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return name(node.value) + "." + node.attr
        return ""

    # Each straight-line scope is isolated. Branches/loops are intentionally unresolved,
    # rather than promoting a speculative reaching definition to a confirmed edge.
    def scope(body: list[ast.stmt], aliases: dict[str, str], shadowed: set[str]) -> None:
        values: dict[str, set[str]] = {}

        def value(expr: ast.AST) -> set[str]:
            if isinstance(expr, ast.Name):
                return values.get(expr.id, set())
            if isinstance(expr, ast.Call):
                called = name(expr.func)
                head, _, tail = called.partition(".")
                called = aliases.get(head, head) + ("." + tail if tail else "")
                strings = [
                    n.value.lower()
                    for n in ast.walk(expr)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str)
                ]
                sensitive = any(
                    any(
                        k in s
                        for k in ("secret", "token", "password", "api_key", ".ssh/", "credentials")
                    )
                    for s in strings
                )
                if sensitive and (
                    (called == "open" and "open" not in shadowed)
                    or (head in aliases and called in {"os.getenv", "os.environ.get"})
                ):
                    src = emit("Read", expr, "secret")
                    if called != "os.getenv" and called != "os.environ.get":
                        emit("StrongSecret", expr)
                    return {src}
                if head in aliases and called in {
                    "requests.post",
                    "httpx.post",
                    "requests.put",
                    "httpx.put",
                }:
                    dst = emit("Net", expr, "out")
                    # Authentication headers are not exfiltration payloads.
                    payload = [k.value for k in expr.keywords if k.arg in {"data", "json", "files"}]
                    if len(expr.args) > 1:
                        payload.append(expr.args[1])
                    for arg in payload:
                        for src in value(arg):
                            facts.append(
                                Fact(
                                    "StrongSecret",
                                    (src,),
                                    span=span(arg),
                                    extractor="python-ast-payload",
                                )
                            )
                            facts.append(
                                Fact(
                                    "ConfirmedFlow",
                                    (src, dst),
                                    span=span(arg),
                                    extractor="python-ast",
                                )
                            )
                    return set()
                if isinstance(expr.func, ast.Attribute) and expr.func.attr == "read":
                    return value(expr.func.value)
                # An unknown function can transform, discard or replace its argument.
                return set()
            if isinstance(
                expr, (ast.Dict, ast.List, ast.Tuple, ast.Set, ast.JoinedStr, ast.FormattedValue)
            ):
                return set().union(*(value(child) for child in ast.iter_child_nodes(expr)))
            return set()

        for stmt in body:
            if isinstance(stmt, ast.Import):
                for item in stmt.names:
                    aliases[item.asname or item.name] = item.name
            elif isinstance(stmt, ast.ImportFrom):
                for item in stmt.names:
                    aliases[item.asname or item.name] = f"{stmt.module}.{item.name}"
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = stmt.args
                parameters = {a.arg for a in [*args.posonlyargs, *args.args, *args.kwonlyargs]}
                if args.vararg:
                    parameters.add(args.vararg.arg)
                if args.kwarg:
                    parameters.add(args.kwarg.arg)
                scope(
                    stmt.body,
                    {k: v for k, v in aliases.items() if k not in parameters},
                    shadowed | parameters,
                )
                aliases.pop(stmt.name, None)
                shadowed.add(stmt.name)
            elif isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                sources = value(stmt.value) if stmt.value else set()
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        values[target.id] = sources
                        aliases.pop(target.id, None)
                        shadowed.add(target.id)
            elif isinstance(stmt, ast.Expr):
                value(stmt.value)
            else:
                # Unknown control flow invalidates simple reaching definitions.
                values.clear()

    scope(tree.body, {}, set())
    return facts
