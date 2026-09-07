"""Fetch real skill samples from MaliciousAgentSkillsBench into the benchmark corpus.

The dataset (Liu et al., "Do Not Mention This to the User", MIT licence) ships verdict
labels for 98,380 real skills together with download URLs, redacted only for repositories
that host confirmed-malicious skills. That makes it the only openly-licensed source of
*real* labelled skill content, so the benign and suspicious halves of our benchmark are
drawn from it rather than written by hand.

Deterministic: sampling is seeded, so re-running reproduces the same corpus.

    python scripts/fetch_upstream.py --benign 12 --suspicious 15
"""

from __future__ import annotations

import argparse
import csv
import io
import random
import re
import shutil
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

ZENODO_ZIP = "https://zenodo.org/records/20286334/files/protectskills/MaliciousAgentSkillsBench-v0.2.zip?download=1"
CACHE = Path(".cache/upstream")
CORPUS = Path("benchmark/corpus")
SEED = 20260907

# Skills whose content we will not redistribute even though the dataset links them.
MAX_SAMPLE_BYTES = 256 * 1024


@dataclass(frozen=True)
class Row:
    source: str
    repo: str
    skill_name: str
    classification: str
    url: str

    @property
    def sample_id(self) -> str:
        owner, repo = _owner_repo(self.url)
        slug = re.sub(r"[^a-z0-9]+", "-", f"{owner}-{repo}-{self.skill_name}".lower())
        return f"{self.classification}-{slug.strip('-')}"


def _owner_repo(url: str) -> tuple[str, str]:
    m = re.search(r"github\.com/([^/]+)/([^/]+)/archive", url)
    return (m.group(1), m.group(2)) if m else ("unknown", "unknown")


def download(url: str, dest: Path) -> Path:
    """Fetch `url` to `dest`, reusing an existing download."""
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def load_rows() -> list[Row]:
    """Read the ecosystem snapshot out of the cached Zenodo archive."""
    archive = download(ZENODO_ZIP, CACHE / "mabench.zip")
    with zipfile.ZipFile(archive) as zf:
        name = next(n for n in zf.namelist() if n.endswith("data/skills_dataset.csv"))
        text = zf.read(name).decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    return [Row(**{k: r[k] for k in Row.__annotations__}) for r in reader]


def downloadable(rows: list[Row], classification: str) -> list[Row]:
    """Rows of one class whose payload is actually retrievable and uniquely named."""
    seen: set[str] = set()
    out = []
    for r in rows:
        if r.classification != classification or not r.url or r.url.startswith("[REDACTED"):
            continue
        if r.sample_id in seen:
            continue
        seen.add(r.sample_id)
        out.append(r)
    return out


def extract_skill(row: Row, into: Path) -> bool:
    """Pull the one skill directory named by `row` out of its repository archive.

    Returns False when the repository has moved, gone private, or no longer contains a
    skill by that name — the dataset is a snapshot and the ecosystem churns.
    """
    try:
        archive = download(row.url, CACHE / "repos" / f"{row.sample_id}.zip")
    except Exception as exc:
        print(f"  skip {row.sample_id}: {exc}", file=sys.stderr)
        return False

    try:
        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            skill_md = _locate(names, row.skill_name)
            if skill_md is None:
                print(
                    f"  skip {row.sample_id}: no SKILL.md for {row.skill_name!r}", file=sys.stderr
                )
                return False
            root = skill_md.rsplit("/", 1)[0] + "/"
            members = [n for n in names if n.startswith(root) and not n.endswith("/")]
            if sum(zf.getinfo(n).file_size for n in members) > MAX_SAMPLE_BYTES:
                members = [skill_md]  # oversized bundle: keep the instructions only
            into.mkdir(parents=True, exist_ok=True)
            for n in members:
                target = into / n[len(root) :]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(n))
    except zipfile.BadZipFile:
        print(f"  skip {row.sample_id}: not a zip (repo likely gone)", file=sys.stderr)
        return False
    return True


def _locate(names: list[str], skill_name: str) -> str | None:
    """Find the SKILL.md belonging to `skill_name`, preferring an exact directory match."""
    candidates = [n for n in names if n.endswith("/SKILL.md")]
    exact = [n for n in candidates if n.rsplit("/", 2)[-2] == skill_name]
    return (exact or candidates or [None])[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--benign", type=int, default=12)
    ap.add_argument("--suspicious", type=int, default=15)
    ap.add_argument("--force", action="store_true", help="re-extract samples already present")
    args = ap.parse_args()

    rows = load_rows()
    rng = random.Random(SEED)
    fetched: list[Row] = []

    for classification, want in (("safe", args.benign), ("suspicious", args.suspicious)):
        pool = downloadable(rows, classification)
        rng.shuffle(pool)
        print(f"{classification}: {len(pool)} candidates, want {want}")
        for row in pool:
            got = sum(f.classification == classification for f in fetched)
            if got >= want:
                break
            dest = CORPUS / row.sample_id
            if dest.exists() and not args.force:
                fetched.append(row)
                continue
            if dest.exists():
                shutil.rmtree(dest)
            if extract_skill(row, dest):
                print(f"  + {row.sample_id}")
                fetched.append(row)

    print(f"\nfetched {len(fetched)} samples into {CORPUS}")
    print("Next: label them in benchmark/manifest.yaml (verdicts come from the dataset;")
    print("pattern labels need review — record label_source accordingly).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
