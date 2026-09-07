"""Unit tests for the scoring maths, on hand-built samples (no corpus needed)."""

from __future__ import annotations

from skillet.benchmark import Sample
from skillet.evaluator import Detection, evaluate


def _sample(id_: str, verdict: str, patterns=()) -> Sample:
    return Sample(id=id_, verdict=verdict, patterns=tuple(patterns))


def _fixed(mapping: dict[str, Detection]):
    return lambda s: mapping[s.id]


def test_verdict_confusion_counts():
    samples = [
        _sample("a", "malicious"),
        _sample("b", "benign"),
        _sample("c", "suspicious"),
        _sample("d", "benign"),
    ]
    preds = {
        "a": Detection("malicious"),  # tp
        "b": Detection("malicious"),  # fp
        "c": Detection("benign"),  # fn
        "d": Detection("benign"),  # tn
    }
    r = evaluate(samples, _fixed(preds))
    assert (r.verdict.tp, r.verdict.fp, r.verdict.fn) == (1, 1, 1)
    assert r.verdict.precision == 0.5
    assert r.verdict.recall == 0.5


def test_suspicious_counts_as_flag():
    r = evaluate([_sample("a", "suspicious")], _fixed({"a": Detection("suspicious")}))
    assert r.verdict.tp == 1 and r.verdict.fn == 0


def test_per_pattern_scoped_to_present_ids():
    # Gold P1; predicted P1 (tp) + E1 (fp). P3 never appears, so it is not scored at all.
    s = _sample("a", "malicious", ["P1"])
    r = evaluate([s], _fixed({"a": Detection("malicious", frozenset({"P1", "E1"}))}))
    assert r.per_pattern["P1"] == r.per_pattern["P1"].__class__(tp=1, fp=0, fn=0)
    assert r.per_pattern["E1"].fp == 1
    assert "P3" not in r.per_pattern


def test_missed_pattern_is_false_negative():
    s = _sample("a", "malicious", ["P1", "E1"])
    r = evaluate([s], _fixed({"a": Detection("malicious", frozenset({"P1"}))}))
    assert r.per_pattern["E1"].fn == 1


def test_empty_prf_is_zero_not_error():
    r = evaluate([_sample("a", "benign")], _fixed({"a": Detection("benign")}))
    assert r.verdict.precision == 0.0 and r.verdict.f1 == 0.0
