"""Tests for the DSL compiler."""

from __future__ import annotations

import pytest

from skillet.dsl.parser import DslError, compile_rules
from skillet.engine.datalog import Atom, Compare, Neg, Var, evaluate
from skillet.facts.model import Fact, FactSet


def test_library_clause_compiles():
    (rule,) = compile_rules("reaches(A, B) :- edge(A, B).")
    assert rule.head == Atom("Reaches", (Var("A"), Var("B")))
    assert rule.body == (Atom("Edge", (Var("A"), Var("B"))),)


def test_snake_case_maps_to_pascal():
    (rule,) = compile_rules("x(A) :- mentions_external_host(A, H).")
    assert rule.body[0].predicate == "MentionsExternalHost"


def test_rule_block_metadata():
    src = 'rule r severity=HIGH emits=E1 min_confidence=0.5 {\n egress(A)\n => "msg"\n}'
    (rule,) = compile_rules(src)
    assert rule.head == Atom("Alert", ("r",))
    assert rule.severity == "HIGH"
    assert rule.emits == "E1"
    assert rule.min_confidence == 0.5
    assert rule.message == "msg"


def test_negation_and_compare_parse():
    src = "rule r {\n tool(S, T)\n not purpose(S, T)\n A != B\n}"
    (rule,) = compile_rules(src)
    assert any(isinstance(b, Neg) for b in rule.body)
    assert any(isinstance(b, Compare) and b.op == "neq" for b in rule.body)


def test_anonymous_variables_do_not_unify():
    # two `_` in one body must be distinct variables
    src = "rule r {\n host(F, _)\n host(G, _)\n}"
    (rule,) = compile_rules(src)
    anon_names = [
        t.name
        for b in rule.body
        for t in b.terms
        if isinstance(t, Var) and t.name.startswith("_anon")
    ]
    assert len(set(anon_names)) == len(anon_names) == 2


def test_quoted_constant_is_constant():
    (rule,) = compile_rules('rule r {\n mentions_command(F, "base64_decode")\n}')
    assert rule.body[0].terms[1] == "base64_decode"


def test_bad_atom_raises():
    with pytest.raises(DslError):
        compile_rules("rule r {\n this is not an atom\n}")


def test_compiled_rules_run_on_engine():
    rules = compile_rules(
        "reaches(A, B) :- edge(A, B).\n"
        "reaches(A, C) :- reaches(A, B), edge(B, C).\n"
        'rule chain severity=HIGH {\n reaches(x, C)\n => "reachable"\n}'
    )
    fs = FactSet()
    fs.extend([Fact("Edge", ("x", "y")), Fact("Edge", ("y", "z"))])
    res = evaluate(fs, rules)
    assert res.facts.match("Alert")
