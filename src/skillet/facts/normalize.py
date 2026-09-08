"""Text normalisation, so an evasion in the *encoding* cannot hide the content.

Two red-team classes motivate this: security tokens broken up with zero-width characters
or spelled with look-alike (confusable) letters so an ASCII regex misses them, and a
payload isolated behind a huge run of blank lines so the chunker drops it. Both attack the
representation, not the meaning, so the defence is to fold the representation to a canonical
form *before* anything scans it — and to treat the fact that folding was necessary as a
signal in its own right, since honest skills do not hide a zero-width space inside
`AWS_SECRET_ACCESS_KEY`.

Normalisation must not destroy provenance: a fact found in the normalised text still has to
point at a real byte range in the original file. So `Normalized` keeps an index map from
each normalised character back to its source offset, and spans are built through it.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from .model import Span

# Zero-width and invisible formatting characters an attacker inserts to break up a token
# while leaving it visually and semantically intact. Built from codepoints so this source
# file stays pure ASCII (and so the linter need not flag its own defensive data).
_INVISIBLE = {
    chr(cp)
    for cp in (
        0x200B,  # zero-width space
        0x200C,  # zero-width non-joiner
        0x200D,  # zero-width joiner
        0x2060,  # word joiner
        0xFEFF,  # BOM / zero-width no-break space
        0x00AD,  # soft hyphen
        0x180E,  # Mongolian vowel separator
        0x200E,  # left-to-right mark
        0x200F,  # right-to-left mark
    )
}

# Confusable letters (Cyrillic / Greek / other scripts) mapped to their ASCII look-alike.
# Not exhaustive — the common ones an attacker reaches for to spell aws/curl/http/secret.
_CONFUSABLES = {
    chr(cp): ascii_
    for cp, ascii_ in (
        (0x0430, "a"),
        (0x0435, "e"),
        (0x043E, "o"),
        (0x0440, "p"),
        (0x0441, "c"),
        (0x0445, "x"),
        (0x0443, "y"),
        (0x0455, "s"),
        (0x0456, "i"),
        (0x0458, "j"),
        (0x04BB, "h"),
        (0x0501, "d"),
        (0x051B, "q"),
        (0x0261, "g"),
        (0x03BF, "o"),
        (0x03B1, "a"),
        (0x03C1, "p"),
        (0x03BD, "v"),
        (0x03C5, "u"),
        (0x1E05, "b"),
        (0x217C, "l"),
    )
}

MAX_CONSECUTIVE_BLANK = 2  # runs longer than this are a padding attempt


@dataclass(frozen=True)
class Normalized:
    """A canonical form of some text plus the map back to original offsets.

    `to_raw[i]` is the byte offset in the original text of normalised character `i`;
    `to_raw[len(text)]` is the original length, so a half-open normalised range maps cleanly.
    """

    text: str
    to_raw: tuple[int, ...]
    raw: str
    invisible_stripped: int = 0
    confusables_mapped: int = 0
    blank_runs_collapsed: int = 0
    max_blank_run: int = 0  # longest collapsed run — a few blanks is formatting, thousands is hiding

    @property
    def evaded(self) -> bool:
        """Whether normalisation had to undo an evasion (as opposed to no-op)."""
        return bool(self.invisible_stripped or self.confusables_mapped)

    def raw_line_starts(self) -> list[int]:
        starts = [0]
        for i, ch in enumerate(self.raw):
            if ch == "\n":
                starts.append(i + 1)
        return starts

    def span(self, file: str, start: int, end: int, raw_starts: list[int]) -> Span:
        """A Span in *original* coordinates for a match at normalised [start, end)."""
        from bisect import bisect_right

        raw_start = self.to_raw[start]
        raw_end = self.to_raw[min(end, len(self.text))]
        return Span(
            file=file, start=raw_start, end=raw_end, line=bisect_right(raw_starts, raw_start)
        )


def evasion_chars(s: str) -> tuple[bool, bool]:
    """Whether `s` contains (invisible, confusable) characters — used to test whether a
    *specific* matched token was obfuscated, rather than flagging any non-ASCII prose."""
    invisible = any(c in _INVISIBLE for c in s)
    confusable = any(
        c in _CONFUSABLES
        or (unicodedata.normalize("NFKC", c) != c and unicodedata.normalize("NFKC", c).isascii())
        for c in s
    )
    return invisible, confusable


def normalize(raw: str) -> Normalized:
    """Fold `raw` to canonical form, recording the offset map and what was undone."""
    chars: list[str] = []
    to_raw: list[int] = []
    invisible = confus = 0

    # Pass 1: character-level folding (invisible removal, confusable mapping, NFKC width).
    for i, ch in enumerate(raw):
        if ch in _INVISIBLE:
            invisible += 1
            continue
        if ch in _CONFUSABLES:
            chars.append(_CONFUSABLES[ch])
            to_raw.append(i)
            confus += 1
            continue
        folded = unicodedata.normalize("NFKC", ch)
        if folded != ch and len(folded) == 1 and folded.isascii():
            confus += 1
            chars.append(folded)
            to_raw.append(i)
            continue
        chars.append(ch)
        to_raw.append(i)
    to_raw.append(len(raw))

    text = "".join(chars)
    collapsed_text, collapsed_map, runs, max_run = _collapse_blank_runs(text, to_raw)

    return Normalized(
        text=collapsed_text,
        to_raw=tuple(collapsed_map),
        raw=raw,
        invisible_stripped=invisible,
        confusables_mapped=confus,
        blank_runs_collapsed=runs,
        max_blank_run=max_run,
    )


def _collapse_blank_runs(text: str, to_raw: list[int]) -> tuple[str, list[int], int, int]:
    """Collapse runs of >MAX_CONSECUTIVE_BLANK blank lines, keeping the offset map aligned.

    A payload isolated behind thousands of blank lines rejoins its neighbours once the run
    is collapsed, so the chunker no longer drops it into its own sub-minimum window. Returns
    the number of runs collapsed and the length (in lines) of the longest one.
    """
    lines = text.splitlines(keepends=True)
    out_chars: list[str] = []
    out_map: list[int] = []
    pos = 0
    blank_streak = 0
    runs = 0
    max_run = 0
    collapsing = False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank:
            blank_streak += 1
            max_run = max(max_run, blank_streak)
            if blank_streak > MAX_CONSECUTIVE_BLANK:
                if not collapsing:
                    runs += 1
                    collapsing = True
                pos += len(line)
                continue
        else:
            blank_streak = 0
            collapsing = False
        for j, ch in enumerate(line):
            out_chars.append(ch)
            out_map.append(to_raw[pos + j])
        pos += len(line)
    out_map.append(to_raw[len(text)] if text else 0)
    return "".join(out_chars), out_map, runs, max_run
