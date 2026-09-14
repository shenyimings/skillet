"""Static event extraction, optional bounded Pi review, then Datalog with provenance.

V3 is the default. The legacy chunk-labelling client is retired; `legacy=True` keeps the
old static extraction semantics for reproducing historical results. Incomplete semantic
runs never produce a benign verdict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .agent.static import static_facts
from .dsl.parser import compile_rules
from .engine.datalog import Result, Rule, evaluate
from .facts import Tier, extract
from .facts.model import FactSet, Span
from .facts.package import SkillPackage

_CORE_RULES = Path(__file__).parent / "rules" / "core.skl"
_V3_RULES = Path(__file__).parent / "rules" / "v3.skl"

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
    analysis: dict = field(default_factory=dict)

    @property
    def patterns(self) -> set[str]:
        return {a.kind for a in self.alerts if a.kind}


def load_rules(path: Path | None = None) -> list[Rule]:
    """Compile the rule set (the core set by default)."""
    return compile_rules((path or _V3_RULES).read_text())


def scan(
    package: SkillPackage,
    *,
    rules: list[Rule] | None = None,
    agent=None,
    legacy: bool = False,
) -> ScanReport:
    """Scan a snapshot. Pi owns the loop; the host admits facts; rules own verdicts."""
    if agent is not None and legacy:
        raise ValueError("Pi agent and legacy static mode cannot be combined")
    if agent is not None and getattr(agent, "mode", "facts") == "pure":
        facts = FactSet()
        analysis = agent.run(package, facts)
        decision = analysis.get("direct_decision") or {}
        return ScanReport(
            skill=package.name,
            verdict=decision.get("verdict", "unknown"),
            facts=facts,
            analysis=analysis,
        )
    rules = rules if rules is not None else load_rules(_CORE_RULES if legacy else None)

    facts = (
        extract(package, tiers={Tier.AGNOSTIC, Tier.LANGUAGE}) if legacy else static_facts(package)
    )
    analysis = {"status": "static_only", "coverage_complete": False, "load_issues": package.issues}
    if agent is not None:
        analysis = agent.run(package, facts)

    result = evaluate(facts, rules)
    alerts = _collect_alerts(result, rules)
    verdict = _verdict(alerts)
    if not alerts and (
        (
            not legacy
            and (
                agent is None
                or not analysis.get("coverage_complete")
                or result.facts.match("ReviewNeeded")
            )
        )
        or package.issues
    ):
        verdict = "unknown"
    return ScanReport(
        skill=package.name,
        verdict=verdict,
        alerts=alerts,
        facts=facts,
        result=result,
        analysis=analysis,
    )


def scan_path(path: Path | str, *, agent=None, legacy: bool = False) -> ScanReport:
    return scan(SkillPackage.load(path), agent=agent, legacy=legacy)


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
