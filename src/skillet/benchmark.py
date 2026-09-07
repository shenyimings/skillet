"""Load and validate the labelled benchmark.

The manifest is the source of truth for what each sample *is*; the corpus directory holds
what each sample *says*. This module joins them and refuses to proceed if they disagree,
so an evaluation can never silently score against a stale or half-written label set.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = _ROOT / "benchmark"
CORPUS_DIR = BENCHMARK_DIR / "corpus"
MANIFEST = BENCHMARK_DIR / "manifest.yaml"
SCHEMA = BENCHMARK_DIR / "schema" / "manifest.schema.json"

Verdict = str  # one of: benign, suspicious, malicious


@dataclass(frozen=True)
class Sample:
    """One labelled skill in the benchmark, with its files resolved on disk."""

    id: str
    verdict: Verdict
    patterns: tuple[str, ...] = ()
    credential_patterns: tuple[str, ...] = ()
    provenance: str = "synthetic"
    label_source: str = "author_review"
    source_url: str | None = None
    licence: str | None = None
    note: str | None = None
    _dir: Path = field(default=CORPUS_DIR, repr=False)

    @property
    def path(self) -> Path:
        return self._dir / self.id

    @property
    def skill_md(self) -> Path:
        return self.path / "SKILL.md"

    def files(self) -> list[Path]:
        """Every file in the sample, sorted for determinism."""
        return sorted(p for p in self.path.rglob("*") if p.is_file())


class BenchmarkError(RuntimeError):
    """The manifest and corpus are inconsistent."""


def _validate_schema(raw: dict) -> None:
    """Best-effort JSON-Schema check; a no-op if jsonschema is not installed."""
    try:
        import jsonschema
    except ModuleNotFoundError:
        return
    jsonschema.validate(raw, json.loads(SCHEMA.read_text()))


def load(manifest: Path = MANIFEST, corpus: Path = CORPUS_DIR) -> list[Sample]:
    """Return every benchmark sample, validated against schema and corpus.

    Raises BenchmarkError if a labelled sample has no directory, if a directory has no
    SKILL.md, or if a corpus directory is unlabelled — all three are ways a benchmark
    quietly rots, and none should ever pass silently.
    """
    raw = yaml.safe_load(manifest.read_text())
    _validate_schema(raw)

    samples = [
        Sample(
            **{
                **row,
                "patterns": tuple(row.get("patterns", ())),
                "credential_patterns": tuple(row.get("credential_patterns", ())),
                "_dir": corpus,
            }
        )
        for row in raw["samples"]
    ]

    ids = {s.id for s in samples}
    if len(ids) != len(samples):
        raise BenchmarkError("duplicate sample id in manifest")

    for s in samples:
        if not s.path.is_dir():
            raise BenchmarkError(f"{s.id}: labelled but no directory at {s.path}")
        if not s.skill_md.is_file():
            raise BenchmarkError(f"{s.id}: no SKILL.md")

    on_disk = {p.name for p in corpus.iterdir() if p.is_dir()}
    for name in sorted(on_disk - ids):
        raise BenchmarkError(f"{name}: present in corpus but absent from manifest")

    return samples
