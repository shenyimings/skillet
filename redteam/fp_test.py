"""Static FP rate over real benign skills. Non-benign verdict = false positive."""
import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, "/home/user/skillet/src")
# Point at one or more directories of REAL benign skills (e.g. clones of anthropics/skills,
# obra/superpowers, or safe-labelled repos). Pass roots as argv; see redteam/README.md.
import sys as _sys

from skillet.facts.package import SkillPackage
from skillet.pipeline import scan

roots = [Path(a) for a in _sys.argv[1:]] or [Path("benign_corpus")]
skills = []
seen = set()
for r in roots:
    for md in sorted(r.rglob("SKILL.md")):
        d = md.parent
        if d.name in seen:
            continue
        seen.add(d.name)
        skills.append(d)
random.Random(1).shuffle(skills)
skills = skills[:100]
print(f"scanning {len(skills)} real benign skills (static tier)\n")

verdicts = collections.Counter()
rule_fp = collections.Counter()
fps = []
for d in skills:
    try:
        rep = scan(SkillPackage.load(d))
    except Exception as e:
        print("  ERR", d.name, e)
        continue
    verdicts[rep.verdict] += 1
    if rep.verdict != "benign":
        fps.append((d.name, rep.verdict, [a.rule for a in rep.alerts]))
        for a in rep.alerts:
            rule_fp[a.rule] += 1

n = sum(verdicts.values())
fp = n - verdicts["benign"]
print(f"verdicts: {dict(verdicts)}")
print(f"FP rate (flagged / total) = {fp}/{n} = {fp/n:.1%}\n")
print("rules firing on benign (false-positive contributions):")
for rule, c in rule_fp.most_common():
    print(f"  {c:3}  {rule}")
print("\nsample false positives:")
for name, v, rules in fps[:20]:
    print(f"  [{v:9}] {name}: {sorted(set(rules))}")
