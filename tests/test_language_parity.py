"""The multi-language guarantee, as executable tests.

Two claims are checked:

1. The same attack, reimplemented in five languages, yields the same language-invariant
   resource facts — so switching implementation language does not evade detection.
2. Dropping the language-specific (and semantic) tiers never removes a fact the agnostic
   tier established — so language coverage is a floor, not a feature that can regress.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from skillet.facts import Tier, extract, literals
from skillet.facts.package import SkillPackage

POLYGLOT = Path(__file__).parent / "fixtures" / "polyglot"
LANGUAGES = ["steal.py", "steal.js", "steal.go", "steal.rs", "Steal.java"]


def _facts_for(filename: str) -> set[tuple[str, tuple[str, ...]]]:
    text = (POLYGLOT / filename).read_text()
    pkg = SkillPackage(
        name=filename,
        root=POLYGLOT,
        files=[
            _file(filename, text),
        ],
    )
    return {f.key for f in literals.extract(pkg)}


def _file(name: str, text: str):
    from skillet.facts.package import SkillFile

    return SkillFile(path=name, size=len(text.encode()), text=text)


@pytest.mark.parametrize("filename", LANGUAGES)
def test_every_language_reveals_the_same_resources(filename: str):
    keys = _facts_for(filename)
    assert ("MentionsSensitivePath", (filename, "aws_credentials")) in keys, filename
    assert ("MentionsEnvKey", (filename, "AWS_SECRET_ACCESS_KEY")) in keys, filename
    assert ("MentionsExternalHost", (filename, "collector.evil-telemetry.io")) in keys, filename


def test_resource_facts_are_identical_across_languages():
    # Strip the filename (arg 0) so only the resource identity is compared.
    def resources(filename: str) -> set:
        return {(pred, args[1:]) for pred, args in _facts_for(filename)}

    baseline = resources(LANGUAGES[0])
    for other in LANGUAGES[1:]:
        assert resources(other) == baseline, f"{other} differs from {LANGUAGES[0]}"


def test_language_tier_is_additive_only():
    # For every benchmark sample, the agnostic-only fact set must be a subset of the full
    # run: enabling more tiers may add facts or raise confidence, never remove coverage.
    from skillet.benchmark import load

    for sample in load():
        pkg = SkillPackage.load(sample.path)
        agnostic = extract(pkg, tiers={Tier.AGNOSTIC}).keys()
        full = extract(pkg, tiers={Tier.AGNOSTIC, Tier.LANGUAGE, Tier.SEMANTIC}).keys()
        assert agnostic <= full, sample.id
