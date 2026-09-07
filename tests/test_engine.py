"""Tests for the mini-Datalog engine: derivation, closure, negation, provenance."""

from __future__ import annotations

import pytest

from skillet.engine import Atom, Compare, Neg, Result, Rule, StratificationError, Var, evaluate
from skillet.facts.model import Fact, FactSet, Origin, Span

V = Var


def _facts(*facts: Fact) -> FactSet:
    fs = FactSet()
    fs.extend(facts)
    return fs


def _reaches_rules() -> list[Rule]:
    return [
        Rule(Atom("Reaches", (V("a"), V("b"))), (Atom("Edge", (V("a"), V("b"))),), name="base"),
        Rule(
            Atom("Reaches", (V("a"), V("c"))),
            (Atom("Reaches", (V("a"), V("b"))), Atom("Edge", (V("b"), V("c")))),
            name="step",
        ),
    ]


def test_single_rule_derivation():
    fs = _facts(Fact("Edge", ("x", "y")))
    res = evaluate(fs, _reaches_rules())
    assert ("Reaches", ("x", "y")) in res.facts


def test_transitive_closure():
    fs = _facts(Fact("Edge", ("a", "b")), Fact("Edge", ("b", "c")), Fact("Edge", ("c", "d")))
    res = evaluate(fs, _reaches_rules())
    reached = {f.args for f in res.facts.match("Reaches")}
    assert ("a", "d") in reached and ("a", "c") in reached


def test_join_with_shared_variable():
    fs = _facts(
        Fact("Parent", ("alice", "bob")),
        Fact("Parent", ("bob", "carol")),
    )
    rule = Rule(
        Atom("Grandparent", (V("g"), V("c"))),
        (Atom("Parent", (V("g"), V("p"))), Atom("Parent", (V("p"), V("c")))),
        name="gp",
    )
    res = evaluate(fs, [rule])
    assert {f.args for f in res.facts.match("Grandparent")} == {("alice", "carol")}


def test_confidence_is_min_over_chain():
    fs = _facts(
        Fact("A", ("x",), confidence=1.0),
        Fact("B", ("x",), origin=Origin.LLM, confidence=0.6),
    )
    rule = Rule(Atom("C", (V("x"),)), (Atom("A", (V("x"),)), Atom("B", (V("x"),))), name="r")
    res = evaluate(fs, [rule])
    assert res.facts.match("C")[0].confidence == pytest.approx(0.6)


def test_min_confidence_gate_blocks_weak_chains():
    fs = _facts(Fact("B", ("x",), origin=Origin.LLM, confidence=0.4))
    rule = Rule(Atom("C", (V("x"),)), (Atom("B", (V("x"),)),), name="r", min_confidence=0.5)
    assert not evaluate(fs, [rule]).facts.match("C")


def test_negation_as_failure():
    fs = _facts(Fact("Tool", ("s", "net")), Fact("Purpose", ("s", "fs")))
    rule = Rule(
        Atom("Overprivileged", (V("s"), V("t"))),
        (Atom("Tool", (V("s"), V("t"))), Neg(Atom("Purpose", (V("s"), V("t"))))),
        name="op",
    )
    res = evaluate(fs, [rule])
    assert {f.args for f in res.facts.match("Overprivileged")} == {("s", "net")}


def test_compare_neq():
    fs = _facts(Fact("Chunk", ("c1", "f1")), Fact("Chunk", ("c2", "f2")))
    rule = Rule(
        Atom("Pair", (V("a"), V("b"))),
        (
            Atom("Chunk", (V("a"), V("_x"))),
            Atom("Chunk", (V("b"), V("_y"))),
            Compare("neq", V("a"), V("b")),
        ),
        name="pair",
    )
    res = evaluate(fs, [rule])
    assert ("c1", "c1") not in {f.args for f in res.facts.match("Pair")}


def test_stratification_rejects_recursive_negation():
    # p :- not p  has no stratified model.
    rule = Rule(Atom("P", (V("x"),)), (Atom("Q", (V("x"),)), Neg(Atom("P", (V("x"),)))), name="bad")
    with pytest.raises(StratificationError):
        evaluate(_facts(Fact("Q", ("a",))), [rule])


def test_provenance_tree_reaches_source_spans():
    fs = _facts(
        Fact("TargetsSensitive", ("cA", "aws"), span=Span("SKILL.md", 0, 5, 3), extractor="lit"),
        Fact("InFile", ("cA", "SKILL.md")),
        Fact("InFile", ("cB", "ref.md")),
        Fact("Includes", ("SKILL.md", "ref.md"), span=Span("SKILL.md", 10, 20, 5)),
        Fact(
            "Egress",
            ("cB", "evil.io"),
            origin=Origin.LLM,
            confidence=0.8,
            span=Span("ref.md", 0, 4, 1),
        ),
    )
    rules = [
        Rule(
            Atom("Reaches", (V("a"), V("b"))),
            (
                Atom("InFile", (V("a"), V("f1"))),
                Atom("Includes", (V("f1"), V("f2"))),
                Atom("InFile", (V("b"), V("f2"))),
            ),
            name="reaches",
        ),
        Rule(
            Atom("Alert", (V("a"), "exfil")),
            (
                Atom("TargetsSensitive", (V("a"), V("_k"))),
                Atom("Reaches", (V("a"), V("b"))),
                Atom("Egress", (V("b"), V("_h"))),
            ),
            name="exfil",
            severity="HIGH",
        ),
    ]
    res: Result = evaluate(fs, rules)
    alert = res.facts.match("Alert")[0]
    spans = {str(s) for s in res.spans(alert.key)}
    assert spans == {"SKILL.md:3", "SKILL.md:5", "ref.md:1"}
    tree = res.justify(alert.key)
    assert tree.rule == "exfil"
    assert "reaches" in tree.render()


def test_derived_facts_marked_derived():
    fs = _facts(Fact("Edge", ("x", "y")))
    res = evaluate(fs, _reaches_rules())
    derived = res.facts.match("Reaches")[0]
    assert derived.origin is Origin.DERIVED
    assert res.is_derived(derived.key)
