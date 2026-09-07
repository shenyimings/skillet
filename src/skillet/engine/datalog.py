"""A small Datalog with two properties the off-the-shelf engines make awkward.

**Every derived fact remembers why it exists.** A derivation is not a boolean — it is a
tree whose leaves are the source facts (each with a file and byte span) and whose interior
nodes are rule firings. That tree is the entire value proposition over an LLM score: an
alert can be read back as "rule R fired because facts A, B held, and A came from line 12 of
SKILL.md". Provenance is therefore built during evaluation, not reconstructed after.

**Confidence flows through derivations.** A chain is as trustworthy as its weakest link,
so a derived fact's confidence is the minimum over the facts that produced it. Rules can
demand a floor (`min_confidence`), which is how a chain resting only on hedged LLM
assertions is held to a lower severity than one anchored in a parsed literal.

The evaluator is semi-naive with stratified negation — enough for rules that need "…and
the skill does *not* declare this purpose", not more. It operates over hundreds of facts
per skill, so clarity is worth more than asymptotics here.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field

from ..facts.model import Fact, FactKey, FactSet, Origin, Span

# --- Terms, atoms, rules -------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Var:
    """A logic variable. Bare strings in an atom are constants; `Var` binds."""

    name: str

    def __str__(self) -> str:
        return self.name.upper()


Term = Var | str
Binding = Mapping[str, str]


@dataclass(frozen=True, slots=True)
class Atom:
    """A predicate applied to terms, e.g. `Atom("Egress", (Var("C"), Var("H")))`."""

    predicate: str
    terms: tuple[Term, ...]

    def ground(self, binding: Binding) -> tuple[str, ...]:
        """Resolve every term against `binding`; variables must all be bound."""
        return tuple(binding[t.name] if isinstance(t, Var) else t for t in self.terms)


@dataclass(frozen=True, slots=True)
class Neg:
    """Negation as failure over a body atom."""

    atom: Atom


@dataclass(frozen=True, slots=True)
class Compare:
    """A builtin (in)equality between two terms, evaluated on the current binding."""

    op: str  # "eq" | "neq"
    left: Term
    right: Term

    def holds(self, binding: Binding) -> bool:
        left = binding[self.left.name] if isinstance(self.left, Var) else self.left
        right = binding[self.right.name] if isinstance(self.right, Var) else self.right
        return (left == right) if self.op == "eq" else (left != right)


BodyItem = Atom | Neg | Compare


@dataclass(frozen=True, slots=True)
class Rule:
    """`head :- body`. Metadata rides along so a firing can describe itself.

    `emits` names the taxonomy pattern an alert head corresponds to, which is what lets the
    evaluator score the engine per pattern. `min_confidence` refuses to fire on evidence
    weaker than the floor — the lever for demanding stronger support before crying wolf.
    """

    head: Atom
    body: tuple[BodyItem, ...]
    name: str = ""
    severity: str = "MEDIUM"
    message: str = ""
    emits: str = ""
    min_confidence: float = 0.0

    @property
    def positive(self) -> tuple[Atom, ...]:
        return tuple(b for b in self.body if isinstance(b, Atom))


# --- Derivations ---------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Derivation:
    """Why one fact holds: the rule that fired and the facts that satisfied its body."""

    rule: str
    supports: tuple[FactKey, ...]


@dataclass
class Result:
    """The fixpoint plus the provenance needed to explain any fact in it."""

    facts: FactSet
    derivations: dict[FactKey, Derivation] = field(default_factory=dict)
    _source: FactSet | None = None

    def is_derived(self, key: FactKey) -> bool:
        return key in self.derivations

    def justify(self, key: FactKey, _seen: frozenset[FactKey] = frozenset()) -> JustificationNode:
        """Build the full justification tree rooted at `key`."""
        fact = self.facts._by_key.get(key)
        derivation = self.derivations.get(key)
        if derivation is None or key in _seen:
            return JustificationNode(key=key, fact=fact, rule=None, children=())
        children = tuple(self.justify(s, _seen | {key}) for s in derivation.supports)
        return JustificationNode(key=key, fact=fact, rule=derivation.rule, children=children)

    def spans(self, key: FactKey) -> list[Span]:
        """Every source span at the leaves of `key`'s justification, deduplicated."""
        out: set[Span] = set()
        self._collect_spans(key, out, set())
        return sorted(out)

    def _collect_spans(self, key: FactKey, out: set[Span], seen: set[FactKey]) -> None:
        if key in seen:
            return
        seen.add(key)
        derivation = self.derivations.get(key)
        if derivation is None:
            src = self._source if self._source is not None else self.facts
            fact = src._by_key.get(key)
            if fact is not None:
                out.update(src.spans(fact))
            return
        for support in derivation.supports:
            self._collect_spans(support, out, seen)


def _render_key(key: FactKey) -> str:
    return f"{key[0]}({', '.join(key[1])})"


@dataclass(frozen=True, slots=True)
class JustificationNode:
    """One node of a justification tree; leaves have `rule is None`."""

    key: FactKey
    fact: Fact | None
    rule: str | None
    children: tuple[JustificationNode, ...]

    def render(self, indent: int = 0) -> str:
        pad = "  " * indent
        head = str(self.fact) if self.fact is not None else _render_key(self.key)
        label = f"{pad}{head}" + (f"  [{self.rule}]" if self.rule else "")
        return "\n".join([label, *(c.render(indent + 1) for c in self.children)])


# --- Evaluation ----------------------------------------------------------------------


class StratificationError(ValueError):
    """The rule set mixes negation and recursion in a way that has no stratified model."""


def evaluate(source: FactSet, rules: Iterable[Rule]) -> Result:
    """Run `rules` over `source` to a fixpoint, recording every derivation."""
    rules = list(rules)
    strata = _stratify(rules)

    facts = FactSet()
    facts.extend(source)
    derivations: dict[FactKey, Derivation] = {}

    for stratum in strata:
        _saturate(stratum, facts, derivations)

    result = Result(facts=facts, derivations=derivations, _source=source)
    return result


def _saturate(rules: list[Rule], facts: FactSet, derivations: dict[FactKey, Derivation]) -> None:
    """Semi-naive-ish fixpoint for one stratum, mutating `facts`/`derivations` in place."""
    changed = True
    while changed:
        changed = False
        for rule in rules:
            for binding, supports, confidence in _fire(rule, facts):
                args = rule.head.ground(binding)
                key = (rule.head.predicate, args)
                if key in facts:
                    continue
                facts.add(
                    Fact(
                        predicate=rule.head.predicate,
                        args=args,
                        origin=Origin.DERIVED,
                        confidence=confidence,
                        extractor=rule.name or "rule",
                    )
                )
                derivations[key] = Derivation(rule=rule.name, supports=tuple(supports))
                changed = True


def _fire(rule: Rule, facts: FactSet) -> Iterator[tuple[dict[str, str], list[FactKey], float]]:
    """Yield every satisfying binding for `rule`, with its support keys and confidence."""

    def walk(
        items: tuple[BodyItem, ...],
        binding: dict[str, str],
        supports: list[FactKey],
        confidence: float,
    ) -> Iterator[tuple[dict[str, str], list[FactKey], float]]:
        if not items:
            if confidence >= rule.min_confidence:
                yield dict(binding), list(supports), confidence
            return
        item, rest = items[0], items[1:]
        if isinstance(item, Compare):
            if item.holds(binding):
                yield from walk(rest, binding, supports, confidence)
        elif isinstance(item, Neg):
            if not _any_match(item.atom, binding, facts):
                yield from walk(rest, binding, supports, confidence)
        else:
            for fact in facts.match(item.predicate):
                extended = _unify(item.terms, fact.args, binding)
                if extended is None:
                    continue
                yield from walk(
                    rest,
                    extended,
                    [*supports, fact.key],
                    min(confidence, fact.confidence),
                )

    yield from walk(rule.body, {}, [], 1.0)


def _unify(
    terms: tuple[Term, ...], args: tuple[str, ...], binding: Binding
) -> dict[str, str] | None:
    """Extend `binding` so `terms` matches `args`, or None if it cannot."""
    if len(terms) != len(args):
        return None
    out = dict(binding)
    for term, value in zip(terms, args, strict=True):
        if isinstance(term, Var):
            if term.name in out and out[term.name] != value:
                return None
            out[term.name] = value
        elif term != value:
            return None
    return out


def _any_match(atom: Atom, binding: Binding, facts: FactSet) -> bool:
    return any(_unify(atom.terms, f.args, binding) is not None for f in facts.match(atom.predicate))


def _stratify(rules: list[Rule]) -> list[list[Rule]]:
    """Order rules into strata so every negated predicate is fully computed earlier.

    Kahn's algorithm over a predicate graph: a positive body atom is a same-or-earlier
    edge, a negated one a strictly-earlier edge. A negative edge inside a cycle means no
    stratified model exists.
    """
    heads = {r.head.predicate for r in rules}
    # predicate -> set of (dep_predicate, is_negated) it depends on within the rule set
    deps: dict[str, set[tuple[str, bool]]] = {p: set() for p in heads}
    for rule in rules:
        for item in rule.body:
            atom = item.atom if isinstance(item, Neg) else item
            if isinstance(atom, Compare):
                continue
            pred = atom.predicate
            if pred in heads:
                deps[rule.head.predicate].add((pred, isinstance(item, Neg)))

    level: dict[str, int] = {p: 0 for p in heads}
    for _ in range(len(heads) + 1):
        bumped = False
        for pred, edges in deps.items():
            for dep, negated in edges:
                need = level[dep] + (1 if negated else 0)
                if need > level[pred]:
                    level[pred] = need
                    bumped = True
        if not bumped:
            break
    else:
        raise StratificationError("negation inside recursion has no stratified model")

    ordered: dict[int, list[Rule]] = {}
    for rule in rules:
        ordered.setdefault(level[rule.head.predicate], []).append(rule)
    return [ordered[k] for k in sorted(ordered)]
