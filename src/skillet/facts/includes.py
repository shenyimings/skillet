"""The include graph — the input to cross-file reachability.

This is the highest-value static extractor in the system and it parses no code at all. A
skill that reads a credential in `SKILL.md` and exfiltrates it in `reference.md` is two
innocuous documents until you know one points at the other; `Includes` is what makes the
engine's transitive closure possible, and therefore what separates this tool from a
per-file pattern matcher.

References are found by looking for *anything shaped like a path to a file that exists in
the package*, rather than by understanding markdown link syntax, because a skill can point
the agent at a file in prose ("then follow the steps in scripts/deploy.sh") just as
effectively as with a link.
"""

from __future__ import annotations

import re
from collections.abc import Iterator

from .model import Fact, Origin, Span, line_of, line_starts
from .package import SkillPackage

EXTRACTOR = "includes"

# Markdown link/image target, an @-reference, or a bare relative path with an extension.
_MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*\)")
_AT_REF = re.compile(r"(?<![\w`])@([\w./-]+\.[A-Za-z0-9]{1,8})\b")
_BARE_PATH = re.compile(r"(?<![\w`/])((?:\./|\.\./)?(?:[\w-]+/)*[\w.-]+\.[A-Za-z0-9]{1,8})\b")

_EXTERNAL = re.compile(r"\A(?:[a-z][a-z0-9+.-]*:|//|#)", re.I)


def extract(package: SkillPackage) -> Iterator[Fact]:
    """Emit `Includes(src, dst)` for every in-package reference, and flag escapes."""
    for f in package.scannable():
        text = f.text
        assert text is not None
        starts = line_starts(text)
        seen: set[str] = set()

        for pattern, confidence in ((_MD_LINK, 1.0), (_AT_REF, 1.0), (_BARE_PATH, 0.8)):
            for m in pattern.finditer(text):
                target = m.group(1).split("#")[0].strip()
                if not target or _EXTERNAL.match(target):
                    continue
                resolved = package.resolve(f.path, target)
                if resolved is None or resolved == f.path or resolved in seen:
                    continue
                seen.add(resolved)
                yield Fact(
                    predicate="Includes",
                    args=(f.path, resolved),
                    origin=Origin.STATIC,
                    confidence=confidence,
                    span=Span(f.path, m.start(), m.end(), line_of(starts, m.start())),
                    extractor=EXTRACTOR,
                )

    for f in package.files:
        yield Fact("File", (package.name, f.path, f.language_hint), extractor=EXTRACTOR)
        if not f.scannable:
            yield Fact("UnscannableFile", (package.name, f.path), extractor=EXTRACTOR)
            continue
        # Each file is its own locus, so static primitives keyed on the file path join the
        # Flow graph on equal footing with the labeller's chunk loci (which carry
        # InFile(chunk, file)). Without this bridge a static Read and a static Net in the
        # same file could not reach each other.
        yield Fact("InFile", (f.path, f.path), extractor=EXTRACTOR)
