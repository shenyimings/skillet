"""Static event extraction, optional bounded Pi review, then Datalog with provenance.

V3 is the default. Legacy chunk extraction requires explicit legacy=True and is retained
only for reproducibility. Incomplete semantic runs never produce a benign verdict.
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
from .llm.client import Completion
from .llm.labeller import label_package

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
    client: Completion | None = None,
    rules: list[Rule] | None = None,
    passes: int = 1,
    agent=None,
    legacy: bool = False,
) -> ScanReport:
    """Scan a snapshot. Pi owns the loop; the host admits facts; rules own verdicts."""
    if client is not None and not legacy:
        raise ValueError("chunk labelling is retired; use agent=PiAgent(), or explicit legacy=True")
    if agent is not None and legacy:
        raise ValueError("Pi agent and legacy chunk mode cannot be combined")
    rules = rules if rules is not None else load_rules(_CORE_RULES if legacy else None)

    facts = (
        extract(package, tiers={Tier.AGNOSTIC, Tier.LANGUAGE}) if legacy else static_facts(package)
    )
    analysis = {"status": "static_only", "coverage_complete": False, "load_issues": package.issues}
    if client is not None:
        facts.extend(label_package(package, client, passes=passes))
        analysis["status"] = "legacy"
    if agent is not None:
        analysis = agent.run(package, facts)

    result = evaluate(facts, rules)
    alerts = _collect_alerts(result, rules)
    verdict = _verdict(alerts)
    if not alerts and (
        (agent is not None and not analysis.get("coverage_complete")) or package.issues
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


def scan_path(
    path: Path | str, *, client: Completion | None = None, agent=None, legacy: bool = False
) -> ScanReport:
    return scan(SkillPackage.load(path), client=client, agent=agent, legacy=legacy)


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
