"""The fact model — the only thing that crosses from extraction into decision.

Two design commitments live in this module.

**Provenance is structural, not optional.** Every fact records the file and byte range it
came from and which extractor produced it, because the product promise is that an alert
can be walked back to a sentence in a source file. A fact with no way home is a bug.

**Origin is a first-class discriminator.** A `NetCall` recovered by a parser and one
asserted by the semantic labeller are the same predicate but not the same evidence, so
rules can require a minimum confidence or a particular origin. This is what buys back the
reliability we would otherwise have bought with per-language grammars.
"""

from __future__ import annotations

from bisect import bisect_right
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field, replace
from enum import StrEnum


class Origin(StrEnum):
    """How a fact came to be known."""

    STATIC = "static"  # a parser derived it; deterministic and exact
    LLM = "llm"  # the labeller asserted it; probabilistic and attackable
    DERIVED = "derived"  # an engine rule produced it from other facts


@dataclass(frozen=True, slots=True, order=True)
class Span:
    """A byte range inside one file of the skill package."""

    file: str
    start: int
    end: int
    line: int = 0

    @classmethod
    def locate(cls, file: str, text: str, start: int, end: int) -> Span:
        """Build a span, computing the 1-based line number of `start`."""
        return cls(
            file=file,
            start=len(text[:start].encode()),
            end=len(text[:end].encode()),
            line=text.count("\n", 0, start) + 1,
        )

    def excerpt(self, text: str, limit: int = 120) -> str:
        """The source text this span covers, collapsed to one line for reporting."""
        raw = " ".join(text.encode()[self.start : self.end].decode(errors="replace").split())
        return raw if len(raw) <= limit else raw[: limit - 1] + "…"

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


# A fact's identity for Datalog purposes: the same tuple asserted twice is one fact,
# however many places it was seen. Evidence accumulates on it rather than duplicating it.
FactKey = tuple[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class Fact:
    """One ground atom, plus where it came from and how much to trust it."""

    predicate: str
    args: tuple[str, ...]
    origin: Origin = Origin.STATIC
    confidence: float = 1.0
    span: Span | None = None
    extractor: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence out of range: {self.confidence}")

    @property
    def key(self) -> FactKey:
        return (self.predicate, self.args)

    def __str__(self) -> str:
        args = ", ".join(self.args)
        where = f" @{self.span}" if self.span else ""
        return f"{self.predicate}({args}){where}"


@dataclass
class FactSet:
    """Facts indexed for matching, deduplicated by key, with evidence accumulated.

    Deduplication matters: the same host mentioned in five places is one fact supported by
    five spans, not five facts. Rules should fire once, and the report should list all
    five.
    """

    _by_key: dict[FactKey, Fact] = field(default_factory=dict)
    _evidence: dict[FactKey, list[Fact]] = field(default_factory=lambda: defaultdict(list))
    _by_predicate: dict[str, set[FactKey]] = field(default_factory=lambda: defaultdict(set))

    def add(self, fact: Fact) -> None:
        """Assert `fact`, merging into any existing assertion of the same tuple.

        The retained fact keeps the strongest evidence: highest confidence wins, and a
        static derivation outranks an LLM assertion at equal confidence.
        """
        key = fact.key
        self._evidence[key].append(fact)
        self._by_predicate[fact.predicate].add(key)
        current = self._by_key.get(key)
        if current is None or _outranks(fact, current):
            self._by_key[key] = fact

    def extend(self, facts: Iterable[Fact]) -> None:
        for f in facts:
            self.add(f)

    def match(self, predicate: str) -> list[Fact]:
        """Every distinct fact for `predicate`, in insertion-stable sorted order."""
        return [self._by_key[k] for k in sorted(self._by_predicate.get(predicate, ()))]

    def evidence(self, fact: Fact) -> list[Fact]:
        """Every assertion supporting `fact`, including the one that was retained."""
        return list(self._evidence.get(fact.key, ()))

    def spans(self, fact: Fact) -> list[Span]:
        """Distinct source locations supporting `fact`, sorted."""
        return sorted({e.span for e in self.evidence(fact) if e.span is not None})

    def without_origin(self, origin: Origin) -> FactSet:
        """A copy with every assertion of `origin` dropped.

        This exists to make the multi-language guarantee testable: dropping every
        language-specific static derivation must not change any verdict, only its
        confidence. See tests/test_language_parity.py.
        """
        out = FactSet()
        for evidence in self._evidence.values():
            out.extend(e for e in evidence if e.origin is not origin)
        return out

    def without_extractor(self, *names: str) -> FactSet:
        """A copy with every assertion from the named extractors dropped."""
        dropped = set(names)
        out = FactSet()
        for evidence in self._evidence.values():
            out.extend(e for e in evidence if e.extractor not in dropped)
        return out

    def keys(self) -> set[FactKey]:
        return set(self._by_key)

    def predicates(self) -> set[str]:
        return {p for p, keys in self._by_predicate.items() if keys}

    def __iter__(self) -> Iterator[Fact]:
        return iter(self._by_key.values())

    def __len__(self) -> int:
        return len(self._by_key)

    def __contains__(self, item: Fact | FactKey) -> bool:
        return (item.key if isinstance(item, Fact) else item) in self._by_key


def _outranks(candidate: Fact, incumbent: Fact) -> bool:
    """Whether `candidate` is better evidence than `incumbent` for the same tuple."""
    if candidate.confidence != incumbent.confidence:
        return candidate.confidence > incumbent.confidence
    return candidate.origin is Origin.STATIC and incumbent.origin is Origin.LLM


def downgrade(fact: Fact, confidence: float) -> Fact:
    """A copy of `fact` at a lower confidence, keeping its provenance."""
    return replace(fact, confidence=min(fact.confidence, confidence))


__all__ = ["Fact", "FactKey", "FactSet", "Origin", "Span", "downgrade"]


def line_starts(text: str) -> list[int]:
    """Offsets of each line start, for callers converting many offsets to line numbers."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def line_of(starts: list[int], offset: int) -> int:
    """1-based line number for `offset` given precomputed `line_starts`."""
    return bisect_right(starts, offset)
