"""skillet command line.

Only the benchmark-facing commands exist yet, because benchmark and evaluator come before
the engine. `scan` is a deliberate stub so the surface is visible but nothing pretends to
work before it does.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from . import baselines
from .benchmark import load
from .detector import engine_detector
from .evaluator import Report, evaluate
from .pipeline import scan_path

app = typer.Typer(add_completion=False, help="Security detector for LLM agent skills.")
console = Console()

_DETECTORS = {
    "keyword": baselines.keyword_baseline,
    "always-benign": baselines.always_benign,
    "engine-static": engine_detector(use_llm=False),
    "engine-llm": engine_detector(use_llm=True),
}


def _render(report: Report, detector: str) -> None:
    v = report.verdict
    console.print(
        f"[bold]{detector}[/bold] over {report.n_samples} samples  "
        f"verdict P={v.precision:.2f} R={v.recall:.2f} F1={v.f1:.2f}"
    )
    table = Table(title="per-pattern", show_edge=False)
    for col in ("pattern", "tp", "fp", "fn", "precision", "recall", "f1"):
        table.add_column(col, justify="right" if col != "pattern" else "left")
    for pid, prf in report.per_pattern.items():
        table.add_row(
            pid,
            str(prf.tp),
            str(prf.fp),
            str(prf.fn),
            f"{prf.precision:.2f}",
            f"{prf.recall:.2f}",
            f"{prf.f1:.2f}",
        )
    console.print(table)
    console.print(f"macro pattern F1: {report.macro_pattern_f1:.2f}")


@app.command()
def bench(
    detector: str = typer.Option("keyword", help=f"one of {sorted(_DETECTORS)}"),
) -> None:
    """Score a detector against the labelled benchmark."""
    if detector not in _DETECTORS:
        raise typer.BadParameter(f"unknown detector {detector!r}; choose from {sorted(_DETECTORS)}")
    _render(evaluate(load(), _DETECTORS[detector]), detector)


@app.command(name="list")
def list_samples() -> None:
    """List benchmark samples with their verdict and provenance."""
    table = Table(show_edge=False)
    for col in ("id", "verdict", "patterns", "provenance"):
        table.add_column(col)
    for s in load():
        table.add_row(s.id, s.verdict, ",".join(s.patterns) or "-", s.provenance)
    console.print(table)


@app.command()
def scan(
    path: str,
    llm: bool = typer.Option(False, "--llm", help="also run the semantic (LLM) tier"),
    show_facts: bool = typer.Option(False, help="print the derived fact base"),
) -> None:
    """Scan a skill directory and print an audited report."""
    client = None
    if llm:
        from .llm.client import DeepSeekClient

        client = DeepSeekClient()
    report = scan_path(path, client=client)

    colour = {"benign": "green", "suspicious": "yellow", "malicious": "red"}[report.verdict]
    console.print(f"\n[bold]{report.skill}[/bold]: [{colour}]{report.verdict.upper()}[/{colour}]")
    if not report.alerts:
        console.print("  no findings")
    for a in report.alerts:
        where = ", ".join(str(s) for s in a.spans[:4]) or "-"
        console.print(
            f"\n  [{colour}]{a.severity}[/{colour}] {a.rule} "
            f"([cyan]{a.kind or '-'}[/cyan], conf={a.confidence:.2f})"
        )
        console.print(f"    {a.message}")
        console.print(f"    at: {where}")
        console.print("[dim]" + _indent(a.justification, 4) + "[/dim]")

    if show_facts and report.facts is not None:
        console.print("\n[bold]facts[/bold]")
        for f in sorted(report.facts, key=lambda x: (x.predicate, x.args)):
            console.print(f"  {f}  [dim]({f.origin}, {f.confidence:.2f})[/dim]")


def _indent(text: str, n: int) -> str:
    pad = " " * n
    return "\n".join(pad + line for line in text.splitlines())


if __name__ == "__main__":
    app()
