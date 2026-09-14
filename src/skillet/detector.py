"""Adapt the scan pipeline to the evaluator's detector interface.

The evaluator scores any `Sample -> Detection` callable, so this is the thin shim that lets
the real engine be measured on the benchmark on the same footing as the baselines.
"""

from __future__ import annotations

from collections.abc import Callable

from .benchmark import Sample
from .evaluator import Detection
from .pipeline import scan


def engine_detector() -> Callable[[Sample], Detection]:
    """A detector backed by the static pipeline: deterministic, offline, no API key.

    Semantic review is a bounded per-skill Pi run, not an unbounded batch benchmark.
    """

    def detect(sample: Sample) -> Detection:
        from .facts.package import SkillPackage

        report = scan(SkillPackage.load(sample.path))
        return Detection(verdict=report.verdict, patterns=frozenset(report.patterns))

    return detect
