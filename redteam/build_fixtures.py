"""Materialise generated red-team fixtures that are too large to keep in git.

The oversized-file attack needs a >1 MiB script to exercise skillet's read cap, but a 2 MiB
blob has no place in version control. So the real payload lives in a small committed seed
(`collect_seed.py`) and this builder pads it past the cap on demand. The inflated
`collect.py` is gitignored; `redteam/run.py` and the tests call `build()` before scanning.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OVERSIZED = ROOT / "attacks" / "r1-oversized-file" / "tools"
TARGET_BYTES = 1_990_000  # comfortably over MAX_FILE_BYTES (1 MiB)


def build() -> None:
    """(Re)generate every large fixture that is not stored in git."""
    _build_oversized()


def _build_oversized() -> None:
    seed = (OVERSIZED / "collect_seed.py").read_text()
    out = OVERSIZED / "collect.py"
    if out.exists() and out.stat().st_size >= TARGET_BYTES:
        return
    pad_line = "# aws-price-datum " * 6 + "\n"
    pad = pad_line * (TARGET_BYTES // len(pad_line) + 1)
    # Payload first (so the read-cap prefix still sees it), then the padding blob.
    out.write_text(seed + '\n\n_PRICE_TABLE = """\n' + pad + '"""\n')


if __name__ == "__main__":
    build()
    print("fixtures built")
