"""Scan every red-team attack and report which ones skillet catches.

Every attack here is malicious by construction, so `benign` is a bypass. Static tier by
default; pass --llm to also run the semantic tier (needed for attacks that target the
labeller rather than the static scanner).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_fixtures

from skillet.facts.package import SkillPackage
from skillet.pipeline import scan

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.yaml"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--llm", action="store_true", help="also run the semantic tier")
    ap.add_argument("--round", type=int, help="only this round")
    args = ap.parse_args()
    build_fixtures.build()

    client = None
    if args.llm:
        from skillet.llm.client import DeepSeekClient

        client = DeepSeekClient()

    entries = yaml.safe_load(MANIFEST.read_text())["attacks"] if MANIFEST.exists() else []
    rows = []
    bypassed = []
    for e in entries:
        if args.round and e.get("round") != args.round:
            continue
        path = ROOT / "attacks" / e["id"]
        if not path.is_dir():
            rows.append((e["id"], e.get("technique", ""), "MISSING", "-"))
            continue
        use_client = client if (args.llm or not e.get("needs_llm")) else None
        report = scan(SkillPackage.load(path), client=use_client)
        caught = report.verdict != "benign"
        result = "caught" if caught else "BYPASS"
        rows.append((e["id"], e.get("technique", ""), report.verdict, result))
        if not caught:
            bypassed.append(e["id"])

    w = max((len(r[0]) for r in rows), default=10)
    print(f"{'attack':<{w}}  {'technique':<34}  {'verdict':<10}  result")
    print("-" * (w + 60))
    for aid, tech, verdict, result in rows:
        print(f"{aid:<{w}}  {tech[:34]:<34}  {verdict:<10}  {result}")

    print(f"\n{len(rows)} attacks, {len(bypassed)} bypassed skillet")
    if bypassed:
        print("BYPASS:", ", ".join(bypassed))
    return 1 if bypassed else 0


if __name__ == "__main__":
    raise SystemExit(main())
