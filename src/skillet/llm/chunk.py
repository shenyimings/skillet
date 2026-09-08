"""Splitting a skill into independently-labelled chunks.

Two constraints shape this. First, the labeller sees one chunk at a time and never the
whole file, so an injection buried in section 9 cannot reach across and rewrite how section
2 is labelled. Second, every chunk keeps the byte offset of its start in its origin file,
so a fact the labeller asserts about a chunk can be turned back into a real `Span` — the
semantic tier is held to the same provenance standard as everything else.

Chunking follows the document's own structure: Markdown is split at headings and fenced
code blocks (a code block is its own chunk, because it is a different kind of evidence);
other text files are split into bounded windows. The goal is chunks small enough that a
span is meaningful, large enough that an instruction and its object stay together.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise

from ..facts.package import SkillFile, SkillPackage

MAX_CHUNK_CHARS = 1500
MIN_CHUNK_CHARS = 40


class ChunkKind(StrEnum):
    PROSE = "prose"
    CODE = "code"


@dataclass(frozen=True, slots=True)
class Chunk:
    """A labelable unit, addressable back to its source."""

    id: str
    file: str
    kind: ChunkKind
    text: str
    start: int  # byte offset of chunk start within its file
    language: str = "unknown"

    @property
    def end(self) -> int:
        return self.start + len(self.text.encode("utf-8"))


_FENCE = re.compile(r"^([ \t]*)(`{3,}|~{3,})([^\n]*)\n(.*?)(?:^\1\2[ \t]*$|\Z)", re.M | re.S)
_HEADING = re.compile(r"^#{1,6}[ \t].*$", re.M)


def chunk_package(package: SkillPackage) -> list[Chunk]:
    """Every chunk of every scannable file, entrypoint first."""
    chunks: list[Chunk] = []
    for f in package.scannable():
        chunks.extend(chunk_file(f))
    return chunks


def chunk_file(f: SkillFile) -> list[Chunk]:
    if f.text is None:
        return []
    # Chunk the *normalised* text: blank-run collapse means a payload isolated behind
    # thousands of blank lines rejoins its neighbours instead of landing in a sub-minimum
    # window that gets dropped. Chunk offsets are mapped back to raw bytes for spans.
    norm = f.norm
    text = norm.text
    if f.suffix in (".md", ".markdown", ".mdx"):
        pieces = _split_markdown(text)
    else:
        pieces = _split_plain(text, kind=_kind_for(f), language=f.language_hint)

    # Section chunking splits at headings, so an instruction deliberately straddling a
    # heading is torn in half and neither piece reads as an instruction. A second pass of
    # overlapping windows over the whole prose keeps such an instruction intact in some
    # window, closing the split-injection gap without giving up per-chunk independence.
    if _kind_for(f) is ChunkKind.PROSE or f.suffix in (".md", ".markdown", ".mdx"):
        pieces = [*pieces, *_overlapping_windows(text)]

    out: list[Chunk] = []
    for i, (kind, start, body, lang) in enumerate(pieces):
        if len(body.strip()) < MIN_CHUNK_CHARS and kind is ChunkKind.PROSE:
            continue
        raw_start = norm.to_raw[min(start, len(text))]
        out.append(
            Chunk(
                id=f"{f.path}#{i}",
                file=f.path,
                kind=kind,
                text=body,
                start=raw_start,
                language=lang,
            )
        )
    return out


def _overlapping_windows(text: str) -> list[tuple[ChunkKind, int, str, str]]:
    """Half-overlapping windows over the whole text, so a heading-straddling instruction
    survives intact in at least one window."""
    step = MAX_CHUNK_CHARS // 2
    if len(text) <= step:
        return []
    out: list[tuple[ChunkKind, int, str, str]] = []
    for start in range(0, len(text), step):
        body = text[start : start + MAX_CHUNK_CHARS]
        if body.strip():
            out.append((ChunkKind.PROSE, start, body, "markdown"))
        if start + MAX_CHUNK_CHARS >= len(text):
            break
    return out


def _kind_for(f: SkillFile) -> ChunkKind:
    prose = {"markdown", "unknown", "yaml", "json", "toml"}
    return ChunkKind.PROSE if f.language_hint in prose else ChunkKind.CODE


def _split_markdown(text: str) -> list[tuple[ChunkKind, int, str, str]]:
    """Split at fenced code blocks; prose between fences is split further at headings."""
    pieces: list[tuple[ChunkKind, int, str, str]] = []
    cursor = 0
    for m in _FENCE.finditer(text):
        if m.start() > cursor:
            pieces.extend(_split_prose(text[cursor : m.start()], cursor))
        info = m.group(3).strip().split()
        language = info[0].lower() if info else "unknown"
        pieces.extend(
            (ChunkKind.CODE, m.start(4) + off, body, language)
            for off, body in _window(m.group(4), MAX_CHUNK_CHARS)
        )
        cursor = m.end()
    if cursor < len(text):
        pieces.extend(_split_prose(text[cursor:], cursor))
    return pieces


def _split_prose(text: str, base: int) -> list[tuple[ChunkKind, int, str, str]]:
    """Split prose at markdown headings, then window anything still too large."""
    starts = [m.start() for m in _HEADING.finditer(text)]
    bounds = [0, *[s for s in starts if s > 0], len(text)]
    bounds = sorted(set(bounds))
    out: list[tuple[ChunkKind, int, str, str]] = []
    for a, b in pairwise(bounds):
        segment = text[a:b]
        out.extend(
            (ChunkKind.PROSE, base + a + off, body, "markdown")
            for off, body in _window(segment, MAX_CHUNK_CHARS)
        )
    return out


def _split_plain(
    text: str, kind: ChunkKind, language: str
) -> list[tuple[ChunkKind, int, str, str]]:
    return [(kind, off, body, language) for off, body in _window(text, MAX_CHUNK_CHARS)]


def _window(text: str, size: int) -> list[tuple[int, str]]:
    """Break `text` into <=size windows at line boundaries, keeping start offsets."""
    if len(text) <= size:
        return [(0, text)] if text.strip() else []
    out: list[tuple[int, str]] = []
    lines = text.splitlines(keepends=True)
    buf: list[str] = []
    buf_start = 0
    pos = 0
    for line in lines:
        if buf and sum(len(x) for x in buf) + len(line) > size:
            out.append((buf_start, "".join(buf)))
            buf, buf_start = [], pos
        if not buf:
            buf_start = pos
        buf.append(line)
        pos += len(line)
    if buf:
        out.append((buf_start, "".join(buf)))
    return [(s, b) for s, b in out if b.strip()]
