"""Regression tests for the round-1 red-team hardening.

Each test pins one bypass class closed. They run on the static tier (deterministic, no
network); the chunk-split injection is semantic and is verified separately with a scripted
labeller in test_pipeline, plus live in the red-team notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

from skillet.facts import extract
from skillet.facts.normalize import normalize
from skillet.facts.package import SkillFile, SkillPackage
from skillet.pipeline import scan_path

ROOT = Path(__file__).resolve().parents[1]
ATTACKS = ROOT / "redteam" / "attacks"

sys.path.insert(0, str(ROOT / "redteam"))
import build_fixtures  # noqa: E402

build_fixtures.build()


def _pkg(text: str, name: str = "SKILL.md") -> SkillPackage:
    return SkillPackage(name="t", root=ATTACKS, files=[SkillFile(name, len(text.encode()), text)])


# --- normalisation unit tests --------------------------------------------------------


def test_zero_width_is_stripped_and_flagged():
    n = normalize("AWS_SEC​RET_ACCESS_KEY")
    assert "AWS_SECRET_ACCESS_KEY" in n.text
    assert n.invisible_stripped == 1 and n.evaded


def test_confusable_is_folded():
    n = normalize("сurl")  # Cyrillic es + url
    assert n.text == "curl" and n.confusables_mapped == 1


def test_offset_maps_back_to_raw():
    raw = "x​.aws/credentials"
    n = normalize(raw)
    i = n.text.find(".aws")
    assert raw[n.to_raw[i]] == "."


def test_blank_run_collapse_preserves_payload():
    raw = "top\n" + "\n" * 3000 + "hidden\n"
    n = normalize(raw)
    assert "hidden" in n.text and n.blank_runs_collapsed == 1
    assert len(n.text) < 100


# --- end-to-end bypass regressions (static tier) -------------------------------------


def test_unicode_confusable_attack_is_caught():
    assert scan_path(ATTACKS / "r1-unicode-confusable").verdict != "benign"


def test_constructed_endpoint_needs_the_semantic_tier():
    # A single named env var read + a runtime-built host is exactly the API-client shape
    # that must NOT trip the static tier (that shape is where the benign FP lived). Static
    # sees Net(out) but no strong secret, so it stays benign; the reviewer classifying the
    # read as sensitive is what escalates it. Verified deterministically through the real
    # host observe admission path.
    from skillet.agent import AgentHost
    from skillet.engine.datalog import evaluate
    from skillet.facts.model import FactSet
    from skillet.facts.package import SkillPackage
    from skillet.pipeline import load_rules, scan_path

    assert scan_path(ATTACKS / "r1-constructed-endpoint").verdict == "unknown"

    pkg = SkillPackage.load(ATTACKS / "r1-constructed-endpoint")
    upload = (ATTACKS / "r1-constructed-endpoint" / "tools" / "upload.py").read_text()
    read_q = next(ln.strip() for ln in upload.splitlines() if "environ" in ln)
    send_q = next(ln.strip() for ln in upload.splitlines() if "urlopen" in ln)
    fid = f"f{next(i for i, f in enumerate(pkg.files) if f.path == 'tools/upload.py')}"
    host = AgentHost(pkg, FactSet())
    sources = {}
    for observation, quote in (("reads_sensitive", read_q), ("sends_outward", send_q)):
        start = upload.index(quote)
        result = host.execute(
            "read", {"file": fid, "start": start, "size": len(quote.encode()), "gap": f"code:{fid}"}
        )
        assert "error" not in result["data"]
        sources[observation] = result["data"]["source"]
        result = host.execute(
            "observe",
            {
                "source": result["data"]["source"],
                "label": {"observation": observation, "quote": quote, "confidence": 0.8},
            },
        )
        assert "error" not in result["data"]
    # v3 semantics: co-presence alone yields ReviewNeeded, never an alert.
    result = evaluate(host.facts, load_rules())
    assert result.facts.match("ReviewNeeded") and not result.facts.match("Alert")
    loci = {f.args[1]: f.args[0] for f in host.facts.match("Read") + host.facts.match("Net")}
    edge = host.execute(
        "edge",
        {
            "source_locus": loci["secret"],
            "target_locus": loci["out"],
            "confirmed": True,
            "source": sources["sends_outward"],
            "quote": send_q,
            "reason": "The credential read is embedded in the same outbound request.",
        },
    )
    assert "error" not in edge["data"]
    assert evaluate(host.facts, load_rules()).facts.match("Alert")


def test_include_graph_evasion_is_caught():
    report = scan_path(ATTACKS / "r1-include-graph-evasion")
    assert report.verdict != "benign"
    assert report.facts.match("LexicalHint")
    assert report.facts.match("Net")
    assert report.verdict == "unknown"


def test_whitespace_truncation_is_caught():
    assert scan_path(ATTACKS / "r1-whitespace-truncation").verdict != "benign"


def test_oversized_file_is_caught():
    report = scan_path(ATTACKS / "r1-oversized-file")
    assert report.verdict != "benign"


def test_network_capability_detected_without_host_literal():
    # No URL/IP literal anywhere, but a secret read + a networking API in one file.
    text = "import os, urllib.request\nk = os.environ['API_KEY']\n"
    facts = extract(_pkg(text, "x.py"))
    assert facts.match("Net")
    assert ("Read", ("x.py", "secret")) in facts.keys()


def test_benign_skill_still_passes_after_hardening():
    # The new rules must not turn an innocent skill suspicious.
    report = scan_path(ROOT / "benchmark" / "corpus" / "benign-fixture-safe-skill")
    assert report.verdict == "unknown"
    assert not report.alerts
