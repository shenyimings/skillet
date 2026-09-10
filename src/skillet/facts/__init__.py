"""Fact extraction.

Extractors are tiered, and the tier is not decoration — it is the multi-language
guarantee, made structural:

* `Tier.AGNOSTIC` runs on every file regardless of language and is the only tier allowed
  to establish *coverage*. If an attack is visible at all, it is visible here.
* `Tier.LANGUAGE` is a per-language upgrade (today: Python's stdlib `ast`). It may sharpen
  or corroborate what the agnostic tier already saw. It may never be the sole reason a
  skill is flagged, because then reimplementing the payload in Go would silence us.

`extract(package, tiers=...)` makes that testable: run with `LANGUAGE` withheld and the
verdicts must not move. See `tests/test_language_parity.py`.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from enum import Enum

from . import frontmatter, includes, literals
from .model import Fact, FactSet, Origin, Span
from .package import SkillFile, SkillPackage


class Tier(Enum):
    """What a extractor is allowed to be relied upon for."""

    AGNOSTIC = "agnostic"  # language-independent; establishes coverage
    LANGUAGE = "language"  # language-specific; adds precision only
    SEMANTIC = "semantic"  # the LLM labeller; adds meaning only


Extractor = Callable[[SkillPackage], Iterable[Fact]]

# Ordered: agnostic tier first, so its facts win ties on identical tuples.
REGISTRY: tuple[tuple[str, Tier, Extractor], ...] = (
    ("frontmatter", Tier.AGNOSTIC, frontmatter.extract),
    ("includes", Tier.AGNOSTIC, includes.extract),
    ("literals", Tier.AGNOSTIC, literals.extract),
)

DEFAULT_TIERS = frozenset({Tier.AGNOSTIC, Tier.LANGUAGE})


def extract(
    package: SkillPackage,
    tiers: Iterable[Tier] = DEFAULT_TIERS,
    *,
    behavioral_env: bool = False,
) -> FactSet:
    """Run every registered extractor whose tier is enabled, into one `FactSet`."""
    enabled = frozenset(tiers)
    facts = FactSet()
    for name, tier, extractor in REGISTRY:
        if tier in enabled:
            facts.extend(
                literals.extract(package, behavioral_env=True)
                if name == "literals" and behavioral_env
                else extractor(package)
            )
    return facts


def extractors(tier: Tier) -> Iterator[str]:
    """Names of registered extractors in `tier`."""
    return (name for name, t, _ in REGISTRY if t is tier)


__all__ = [
    "DEFAULT_TIERS",
    "REGISTRY",
    "Extractor",
    "Fact",
    "FactSet",
    "Origin",
    "SkillFile",
    "SkillPackage",
    "Span",
    "Tier",
    "extract",
    "extractors",
]
