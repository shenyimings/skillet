"""Adapt the scan pipeline to the evaluator's detector interface.

The evaluator scores any `Sample -> Detection` callable, so this is the thin shim that lets
the real engine be measured on the benchmark on the same footing as the baselines. A cached
client keeps one connection across a benchmark run when the semantic tier is enabled.
"""

from __future__ import annotations

from collections.abc import Callable

from .benchmark import Sample
from .evaluator import Detection
from .llm.client import Completion
from .pipeline import scan


def engine_detector(
    *, use_llm: bool, client: Completion | None = None
) -> Callable[[Sample], Detection]:
    """A detector backed by the full pipeline.

    With `use_llm=False` the scan is static-only: deterministic, offline, no API key needed.
    With `use_llm=True` a client is constructed lazily (or `client` is used) so importing
    this module never requires credentials.
    """
    resolved: dict[str, Completion | None] = {"client": client}

    def detect(sample: Sample) -> Detection:
        active = None
        if use_llm:
            if resolved["client"] is None:
                from .llm.client import DeepSeekClient

                resolved["client"] = DeepSeekClient()
            active = resolved["client"]
        from .facts.package import SkillPackage

        report = scan(SkillPackage.load(sample.path), client=active)
        return Detection(verdict=report.verdict, patterns=frozenset(report.patterns))

    return detect
