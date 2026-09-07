"""Reference detectors, so the evaluator is runnable before the engine exists.

These are deliberately dumb. They exist to (a) exercise the evaluation harness in tests
and (b) give the eventual Datalog engine a floor to beat. `keyword_baseline` is the
"regex-only" strawman the whole design argues against; measuring it on the benchmark is
the honest way to show what composition-aware detection buys.
"""

from __future__ import annotations

import re

from .benchmark import Sample
from .evaluator import Detection

# (pattern id, compiled regex) pairs over the concatenated skill text. Intentionally
# shallow: single-span, no cross-file reasoning, no semantics.
_KEYWORD_RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "P1",
        re.compile(
            r"ignore (?:all |previous |prior )?(?:instructions|constraints|guidelines)", re.I
        ),
    ),
    ("P3", re.compile(r"\b(?:bcc|forward|send).{0,40}\b(?:context|conversation|history)\b", re.I)),
    ("E1", re.compile(r"requests\.post|curl\s+-|fetch\(|urllib", re.I)),
    ("E2", re.compile(r"os\.environ|API_KEY|SECRET|TOKEN|PASSWORD", re.I)),
    ("E3", re.compile(r"~/\.(?:ssh|aws|config)|id_rsa|credentials", re.I)),
    ("PE1", re.compile(r"bypassPermissions|allowed-tools:\s*Bash\(\*\)|sudo", re.I)),
    ("SC2", re.compile(r"curl\s+[^\n|]*\|\s*(?:sh|bash)|socat|--registry\s+http", re.I)),
    ("SC3", re.compile(r"base64\s+-d|b64decode|eval\(|exec\(", re.I)),
]


def _read_text(sample: Sample) -> str:
    parts = []
    for f in sample.files():
        try:
            parts.append(f.read_text(errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def keyword_baseline(sample: Sample) -> Detection:
    """Flag on any keyword hit; report the matched pattern ids. The strawman."""
    text = _read_text(sample)
    hits = frozenset(pid for pid, rx in _KEYWORD_RULES if rx.search(text))
    verdict = "malicious" if hits else "benign"
    return Detection(verdict=verdict, patterns=hits)


def always_benign(sample: Sample) -> Detection:
    """The trivial lower bound: never flags anything."""
    return Detection(verdict="benign")
