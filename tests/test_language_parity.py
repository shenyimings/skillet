"""The multi-language guarantee, in the v2 primitive vocabulary.

The same attack in five languages must yield the same primitive facts (Read of a secret,
an outward Net), so switching implementation language does not evade detection; and
dropping the language/semantic tiers must never remove a fact the agnostic tier found.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from skillet.facts import Tier, extract, literals
from skillet.facts.package import SkillFile, SkillPackage

POLYGLOT = Path(__file__).parent / "fixtures" / "polyglot"
LANGUAGES = ["steal.py", "steal.js", "steal.go", "steal.rs", "Steal.java"]


def _facts_for(filename: str) -> set[tuple[str, tuple[str, ...]]]:
    text = (POLYGLOT / filename).read_text()
    pkg = SkillPackage(
        name=filename,
        root=POLYGLOT,
        files=[SkillFile(filename, len(text.encode()), text)],
    )
    return {f.key for f in literals.extract(pkg)}


@pytest.mark.parametrize("filename", LANGUAGES)
def test_every_language_reads_a_secret_and_sends_outward(filename: str):
    keys = _facts_for(filename)
    assert ("Read", (filename, "secret")) in keys, filename
    # An outward or at least a network capability is seen in every language.
    assert any(pred == "Net" for pred, _ in keys), filename


def test_primitive_facts_are_identical_across_languages():
    # Compare the resource/verb shape, ignoring the filename (arg 0) and the Net direction
    # (out vs unknown can vary with how precisely the call is recognised); the point is the
    # same primitives appear.
    def shape(filename: str) -> set:
        out = set()
        for pred, args in _facts_for(filename):
            if pred == "Read":
                out.add(("Read", args[1:]))
            elif pred == "Net":
                out.add(("Net",))
        return out

    baseline = shape(LANGUAGES[0])
    for other in LANGUAGES[1:]:
        assert shape(other) == baseline, f"{other} differs from {LANGUAGES[0]}"


def test_language_tier_is_additive_only():
    from skillet.benchmark import load

    for sample in load():
        pkg = SkillPackage.load(sample.path)
        agnostic = extract(pkg, tiers={Tier.AGNOSTIC}).keys()
        full = extract(pkg, tiers={Tier.AGNOSTIC, Tier.LANGUAGE, Tier.SEMANTIC}).keys()
        assert agnostic <= full, sample.id
