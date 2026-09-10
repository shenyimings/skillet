"""Fetch a *wild* corpus of real skills and split it into dev and a sealed held-out set.

Why this exists separately from `fetch_upstream.py`: that script pulls a handful of samples
into the curated benchmark, which is hand-labelled and which the author has read. This one
builds the statistical corpus — hundreds of real skills whose only label is the dataset's
own classification — and, crucially, **splits it before anyone looks at it**.

The split is the point. Rules are written against `dev`; `heldout` is never read, scanned
during development, or reported on until the rule set is frozen. Sealing is by construction:
the sampling, the class-stratified assignment, and the materialisation all happen inside this
script, so no human or agent judgement touches which sample lands where.

Two honest limits, recorded here because they bound what the held-out set can prove:

* The dataset redacts the repositories of confirmed-malicious skills, so **no malicious
  sample is fetchable**. The held-out set contains `safe` and `suspicious` only. It measures
  the false-positive rate and suspicious-recall on unseen data; it cannot measure
  malicious-recall.
* `suspicious` is the dataset's own automated label, not a behavioural confirmation. Treat
  held-out `suspicious` as a weak positive class.

Content is not vendored: these are hundreds of third-party repositories under assorted
licences. The lockfile records repo, commit and path, and the corpus is re-materialised by
cloning, so the split is reproducible without redistributing anyone's code.

    python scripts/fetch_wild.py --safe 150 --suspicious 60
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import random
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_upstream as up

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "wild"
OUT = ROOT / "benchmark" / "wild"
LOCK = ROOT / "benchmark" / "wild.lock.tsv"

SEED = 20260908
HELDOUT_FRACTION = 0.30  # standard held-out share; stratified by class
# A handful of monorepos ship hundreds of skills each. Left uncapped they would supply most
# of the corpus, and the measured rate would describe those repos rather than the ecosystem.
MAX_SKILLS_PER_REPO = 5

# Binary blobs the scanner never reads. Skills ship screenshots, demo GIFs and vendored
# databases; keeping them would put a hundred megabytes of media in the repository without
# adding a byte of scannable content.
SKIP_PATTERNS = (
    ".git",
    "*.duckdb",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "*.parquet",
    "*.zip",
    "*.tar",
    "*.gz",
    "*.tgz",
    "*.whl",
    "*.jar",
    "*.gif",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.webp",
    "*.svg",
    "*.ico",
    "*.bmp",
    "*.mp4",
    "*.mov",
    "*.webm",
    "*.mp3",
    "*.wav",
    "*.pdf",
    "*.woff",
    "*.woff2",
    "*.ttf",
    "*.otf",
    "*.eot",
    "*.pyc",
    "*.so",
    "*.dylib",
    "*.dll",
    "*.wasm",
    "*.node",
)


@dataclass(frozen=True)
class Repo:
    owner: str
    name: str
    classification: str

    @property
    def slug(self) -> str:
        return f"{self.owner}__{self.name}"

    @property
    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.name}.git"


def pick_repos(safe: int, suspicious: int) -> list[Repo]:
    """Seeded, deduplicated sample of repositories with live download URLs.

    Sampling is per repository rather than per skill so that a monorepo of fifty skills
    cannot dominate the corpus, and so that dev and held-out never share a repository (which
    would leak the house style of a prolific author across the split).
    """
    rows = [r for r in up.load_rows() if r.url and "github.com" in r.url]
    by_class: dict[str, dict[tuple[str, str], Repo]] = {"safe": {}, "suspicious": {}}
    for row in rows:
        if row.classification not in by_class:
            continue
        owner, name = up._owner_repo(row.url)
        if owner == "unknown" or not re.fullmatch(r"[\w.-]+", name or ""):
            continue
        by_class[row.classification].setdefault(
            (owner, name), Repo(owner, name, row.classification)
        )

    rng = random.Random(SEED)
    picked: list[Repo] = []
    for cls, want in (("safe", safe), ("suspicious", suspicious)):
        pool = sorted(by_class[cls].values(), key=lambda r: r.slug)
        rng.shuffle(pool)
        picked += pool[:want]
    return picked


def clone(repo: Repo) -> tuple[Repo, str] | None:
    """Shallow-clone `repo` into the cache; return it with its resolved commit."""
    dest = CACHE / repo.classification / repo.slug
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet", repo.url, str(dest)],
            capture_output=True,
            timeout=180,
        )
        if proc.returncode != 0:
            shutil.rmtree(dest, ignore_errors=True)
            return None
    head = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True
    )
    return (repo, head.stdout.strip()) if head.returncode == 0 else None


def skills_in(repo: Repo) -> list[Path]:
    """Up to MAX_SKILLS_PER_REPO skill directories, seeded per repo so the draw is stable."""
    root = CACHE / repo.classification / repo.slug
    found = sorted({p.parent.relative_to(root) for p in root.rglob("SKILL.md")})
    if len(found) <= MAX_SKILLS_PER_REPO:
        return found
    rng = random.Random(f"{SEED}:{repo.slug}")
    return sorted(rng.sample(found, MAX_SKILLS_PER_REPO))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--safe", type=int, default=150)
    ap.add_argument("--suspicious", type=int, default=60)
    args = ap.parse_args()

    repos = pick_repos(args.safe, args.suspicious)
    print(f"selected {len(repos)} repositories; cloning...", flush=True)

    cloned: list[tuple[Repo, str]] = []
    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        for result in pool.map(clone, repos):
            if result:
                cloned.append(result)
    print(f"cloned {len(cloned)}/{len(repos)}", flush=True)

    # Assign the split per repository, stratified by class, before any content is inspected.
    rng = random.Random(SEED + 1)
    entries: list[tuple[str, Repo, str, Path]] = []
    for cls in ("safe", "suspicious"):
        group = [(r, sha) for r, sha in cloned if r.classification == cls]
        group.sort(key=lambda t: t[0].slug)
        rng.shuffle(group)
        cut = round(len(group) * HELDOUT_FRACTION)
        for i, (repo, sha) in enumerate(group):
            split = "heldout" if i < cut else "dev"
            for rel in skills_in(repo):
                entries.append((split, repo, sha, rel))

    if OUT.exists():
        shutil.rmtree(OUT)
    lines = ["split\tclass\trepo\tcommit\tpath"]
    counts: dict[tuple[str, str], int] = {}
    for split, repo, sha, rel in entries:
        sid = f"{repo.slug}__{str(rel).replace('/', '__') or 'root'}"
        dest = OUT / split / repo.classification / sid
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Real repositories carry git-lfs pointers and dangling symlinks; neither is skill
        # content, and a broken link must not abort the materialisation of the whole corpus.
        shutil.copytree(
            CACHE / repo.classification / repo.slug / rel,
            dest,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(*SKIP_PATTERNS),
            ignore_dangling_symlinks=True,
        )
        lines.append(f"{split}\t{repo.classification}\t{repo.owner}/{repo.name}\t{sha}\t{rel}")
        counts[(split, repo.classification)] = counts.get((split, repo.classification), 0) + 1

    LOCK.write_text("\n".join(lines) + "\n")
    print("\nwild corpus:")
    for key in sorted(counts):
        print(f"  {key[0]:8} {key[1]:11} {counts[key]:4}")
    print(f"\nlockfile: {LOCK.relative_to(ROOT)}")
    print("benchmark/wild/heldout/ is SEALED — do not read or scan it during development.")


if __name__ == "__main__":
    main()
