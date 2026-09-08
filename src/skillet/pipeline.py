"""End to end: a skill directory in, an audited report out.

This is the only module that knows the layers exist in a particular order — extract static
facts, optionally label chunks with the LLM, run the rules, read off alerts. Everything it
produces is traceable: an `Alert` names the rule that fired, its severity and pattern, and
the exact source spans that support it.

The semantic tier is optional. With no client, the scan runs on static facts alone — fully
deterministic, offline, and still catches the syntactic patterns. Passing a client adds the
natural-language chain detections. Either way the verdict is derived by the engine, never
by the model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .dsl.parser import compile_rules
from .engine.datalog import Result, Rule, evaluate
from .facts import Tier, extract
from .facts.model import FactSet, Span
from .facts.package import SkillPackage
from .llm.client import Completion
from .llm.labeller import label_package

_CORE_RULES = Path(__file__).parent / "rules" / "core.skl"

# Verdict is the max severity of any alert; these order it.
_SEVERITY_RANK = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
_VERDICT_FOR = {0: "benign", 1: "suspicious", 2: "suspicious", 3: "malicious", 4: "malicious"}


@dataclass(frozen=True)
class Alert:
    """One finding, with everything needed to audit it."""

    rule: str
    kind: str  # taxonomy pattern id emitted, e.g. "E1"
    severity: str
    message: str
    confidence: float
    spans: tuple[Span, ...]
    justification: str  # rendered derivation tree


@dataclass
class ScanReport:
    """The result of scanning one skill."""

    skill: str
    verdict: str
    alerts: list[Alert] = field(default_factory=list)
    facts: FactSet | None = None
    result: Result | None = None

    @property
    def patterns(self) -> set[str]:
        return {a.kind for a in self.alerts if a.kind}


def load_rules(path: Path | None = None) -> list[Rule]:
    """Compile the rule set (the core set by default)."""
    return compile_rules((path or _CORE_RULES).read_text())


def scan(
    package: SkillPackage,
    *,
    client: Completion | None = None,
    rules: list[Rule] | None = None,
    passes: int = 3,
) -> ScanReport:
    """Scan a loaded skill package. With a client, the semantic tier runs too.

    `passes` labels each chunk several times and unions the facts, trading calls for recall
    over the nondeterministic labeller; it only matters when `client` is set.
    """
    rules = rules if rules is not None else load_rules()

    facts = extract(package, tiers={Tier.AGNOSTIC, Tier.LANGUAGE})
    if client is not None:
        facts.extend(label_package(package, client, passes=passes))

    result = evaluate(facts, rules)
    alerts = _collect_alerts(result, rules)
    verdict = _verdict(alerts)
    return ScanReport(
        skill=package.name, verdict=verdict, alerts=alerts, facts=facts, result=result
    )


def scan_path(path: Path | str, *, client: Completion | None = None) -> ScanReport:
    return scan(SkillPackage.load(path), client=client)


def _collect_alerts(result: Result, rules: list[Rule]) -> list[Alert]:
    meta = {r.name: r for r in rules if r.head.predicate == "Alert"}
    alerts: list[Alert] = []
    for fact in result.facts.match("Alert"):
        (name,) = fact.args
        rule = meta.get(name)
        if rule is None:
            continue
        alerts.append(
            Alert(
                rule=name,
                kind=rule.emits,
                severity=rule.severity,
                message=rule.message,
                confidence=fact.confidence,
                spans=tuple(result.spans(fact.key)),
                justification=result.justify(fact.key).render(),
            )
        )
    alerts.sort(key=lambda a: (-_SEVERITY_RANK.get(a.severity, 0), -a.confidence, a.rule))
    return alerts


def _verdict(alerts: list[Alert]) -> str:
    if not alerts:
        return "benign"
    top = max(_SEVERITY_RANK.get(a.severity, 0) for a in alerts)
    return _VERDICT_FOR[top]
