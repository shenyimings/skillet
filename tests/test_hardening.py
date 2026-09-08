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
    # sees Net(out) but no strong secret, so it stays benign; the LLM classifying the read
    # as sensitive is what escalates it. Verified deterministically with a scripted client.
    from skillet.facts.package import SkillPackage
    from skillet.llm import ScriptedClient
    from skillet.pipeline import scan

    assert scan_path(ATTACKS / "r1-constructed-endpoint").verdict == "benign"

    pkg = SkillPackage.load(ATTACKS / "r1-constructed-endpoint")
    upload = (ATTACKS / "r1-constructed-endpoint" / "tools" / "upload.py").read_text()
    read_q = next(ln.strip() for ln in upload.splitlines() if "environ" in ln)
    send_q = next(ln.strip() for ln in upload.splitlines() if "urlopen" in ln)
    client = ScriptedClient(
        {"environ": {"labels": [
            {"observation": "reads_sensitive", "quote": read_q, "confidence": 0.8},
            {"observation": "sends_outward", "quote": send_q, "confidence": 0.8},
        ]}}
    )
    report = scan(pkg, client=client)
    assert report.verdict != "benign"


def test_include_graph_evasion_is_caught():
    report = scan_path(ATTACKS / "r1-include-graph-evasion")
    assert report.verdict != "benign"
    assert any(a.rule.startswith("exfiltration") for a in report.alerts)


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
    assert report.verdict == "benign"
