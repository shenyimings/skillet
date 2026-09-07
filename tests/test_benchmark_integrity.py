"""The benchmark itself must stay consistent: manifest <-> corpus <-> taxonomy."""

from __future__ import annotations

import yaml

from skillet import benchmark
from skillet.baselines import always_benign, keyword_baseline
from skillet.evaluator import evaluate

TAXONOMY = benchmark.BENCHMARK_DIR / "schema" / "taxonomy.yaml"


def test_manifest_loads_and_matches_corpus():
    samples = benchmark.load()
    assert samples, "benchmark is empty"


def test_every_pattern_label_is_defined_in_taxonomy():
    tax = yaml.safe_load(TAXONOMY.read_text())
    valid = {pid for fam in tax["families"].values() for pid in fam["patterns"]}
    valid_cred = set(tax["credential_patterns"])
    for s in benchmark.load():
        assert set(s.patterns) <= valid, f"{s.id}: unknown pattern"
        assert set(s.credential_patterns) <= valid_cred, f"{s.id}: unknown credential pattern"


def test_benign_samples_have_no_expected_patterns():
    for s in benchmark.load():
        if s.verdict == "benign":
            assert not s.patterns and not s.credential_patterns, s.id


def test_corpus_has_all_three_verdicts():
    verdicts = {s.verdict for s in benchmark.load()}
    assert {"benign", "suspicious", "malicious"} <= verdicts


def test_keyword_baseline_runs_and_beats_trivial_recall():
    samples = benchmark.load()
    kw = evaluate(samples, keyword_baseline)
    trivial = evaluate(samples, always_benign)
    # The strawman should at least catch something the do-nothing baseline misses.
    assert kw.verdict.recall > trivial.verdict.recall
