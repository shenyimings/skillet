"""Score the wild corpus, one split at a time.

`dev` is for development: it prints per-sample detail so a false positive can be chased down.
`heldout` deliberately prints **aggregates only** — no sample ids, no file paths, no rule
spans — so that running it cannot become a back door to reading the sealed set. The whole
value of the held-out number is that the rule set was never shaped by it.

    python scripts/eval_wild.py dev
    python scripts/eval_wild.py heldout        # once, after the rules are frozen
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skillet.facts.package import SkillPackage  # noqa: E402
from skillet.pipeline import scan  # noqa: E402

WILD = ROOT / "benchmark" / "wild"


def score(split: str, verbose: bool) -> None:
    root = WILD / split
    if not root.exists():
        sys.exit(f"{root} missing — run scripts/fetch_wild.py first")

    per_class: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    rules: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    detail: list[tuple[str, str, str, list[str]]] = []

    for cls_dir in sorted(root.iterdir()):
        if not cls_dir.is_dir():
            continue
        cls = cls_dir.name
        for sample in sorted(cls_dir.iterdir()):
            if not sample.is_dir():
                continue
            try:
                report = scan(SkillPackage.load(sample))
            except Exception:
                per_class[cls]["error"] += 1
                continue
            per_class[cls][report.verdict] += 1
            for alert in report.alerts:
                rules[cls][alert.rule] += 1
            if report.verdict != "benign":
                detail.append(
                    (cls, sample.name, report.verdict, sorted({a.rule for a in report.alerts}))
                )

    print(f"=== wild/{split} (static tier) ===\n")
    for cls in sorted(per_class):
        counts = per_class[cls]
        n = sum(counts.values())
        flagged = n - counts["benign"] - counts["error"]
        # For `safe`, any non-benign verdict is a false positive. For `suspicious`, a
        # non-benign verdict is a (weak) true positive — the dataset's own label, not a
        # behavioural confirmation, so it is reported as flag-rate rather than recall.
        label = "FP rate" if cls == "safe" else "flag rate"
        print(f"{cls:11} n={n:4}  {dict(counts)}")
        print(f"{'':11} {label} = {flagged}/{n} = {flagged / n:.1%}" if n else "")
        for rule, c in rules[cls].most_common(8):
            print(f"{'':13} {c:4}  {rule}")
        print()

    if verbose:
        print("flagged samples:")
        for cls, name, verdict, rs in detail:
            print(f"  [{cls:10} {verdict:10}] {name}: {rs}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("split", choices=["dev", "heldout"])
    args = ap.parse_args()
    if args.split == "heldout":
        print(
            "Scoring the SEALED held-out set. Aggregates only, by design.\n"
            "Do not use this output to tune rules — that is what the dev split is for.\n"
        )
    score(args.split, verbose=args.split == "dev")


if __name__ == "__main__":
    main()
