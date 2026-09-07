"""Score detector output against the benchmark.

A detector, for our purposes, is any callable that takes a `Sample` and returns a
`Detection`: a verdict plus the set of pattern ids it believes are present. The evaluator
never imports the engine — it scores whatever it is handed, so the same harness measures
the Datalog engine, a regex baseline, or a raw-LLM baseline on equal terms.

Two things are measured, because they answer different questions:

* **Verdict metrics** — treating `suspicious`/`malicious` as "flag" and `benign` as
  "pass", the usual confusion matrix. This is "does it catch bad skills without crying
  wolf".
* **Per-pattern metrics** — precision/recall for each taxonomy pattern id. This is the
  number that tells an analyst whether rule `exfil_chain` is worth keeping, and it is the
  reason the whole system emits pattern ids instead of a scalar score.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

from .benchmark import Sample

FLAG_VERDICTS = {"suspicious", "malicious"}


@dataclass(frozen=True)
class Detection:
    """What a detector concluded about one sample."""

    verdict: str
    patterns: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PRF:
    """Precision / recall / F1 over a set of true/false positives and negatives."""

    tp: int
    fp: int
    fn: int

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0


@dataclass
class Report:
    """The full result of one evaluation run."""

    verdict: PRF
    per_pattern: dict[str, PRF] = field(default_factory=dict)
    confusion: dict[tuple[str, str], int] = field(default_factory=dict)
    n_samples: int = 0

    @property
    def macro_pattern_f1(self) -> float:
        if not self.per_pattern:
            return 0.0
        return sum(p.f1 for p in self.per_pattern.values()) / len(self.per_pattern)


def _flag(verdict: str) -> bool:
    return verdict in FLAG_VERDICTS


def evaluate(
    samples: Iterable[Sample],
    detector: Callable[[Sample], Detection],
) -> Report:
    """Run `detector` over `samples` and return precision/recall at both levels."""
    samples = list(samples)

    v_tp = v_fp = v_fn = 0
    confusion: dict[tuple[str, str], int] = defaultdict(int)
    # pattern id -> [tp, fp, fn]
    pat: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])

    for s in samples:
        d = detector(s)
        confusion[(s.verdict, d.verdict)] += 1

        # Verdict level: flag-vs-pass.
        gold_flag, pred_flag = _flag(s.verdict), _flag(d.verdict)
        if gold_flag and pred_flag:
            v_tp += 1
        elif pred_flag and not gold_flag:
            v_fp += 1
        elif gold_flag and not pred_flag:
            v_fn += 1

        # Pattern level: only over ids that appear in gold or prediction for this sample.
        gold_p, pred_p = set(s.patterns), set(d.patterns)
        for pid in gold_p | pred_p:
            if pid in gold_p and pid in pred_p:
                pat[pid][0] += 1
            elif pid in pred_p:
                pat[pid][1] += 1
            else:
                pat[pid][2] += 1

    return Report(
        verdict=PRF(v_tp, v_fp, v_fn),
        per_pattern={pid: PRF(*counts) for pid, counts in sorted(pat.items())},
        confusion=dict(confusion),
        n_samples=len(samples),
    )
