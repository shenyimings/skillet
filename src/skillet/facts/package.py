"""Loading a skill package off disk.

Deliberately incurious about file types. An attacker choosing an unusual extension — or
none — must not remove a file from analysis, so enumeration is by content, not by name:
every regular file is read, and `is_probably_text` decides whether it can be scanned at
all. Extensions are recorded as a hint for later layers, never used as a gate.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from .normalize import Normalized, normalize

# Read caps. A skill that ships a 10 MB blob is interesting for that fact alone; we record
# it and move on rather than trying to scan it.
MAX_FILE_BYTES = 1 << 20
SKILL_ENTRYPOINT = "SKILL.md"

# Extensions we will *hint* to later layers. Absence from this table means "unknown
# language", which is a valid state and must never mean "skip".
_LANGUAGE_HINTS = {
    ".py": "python",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".ps1": "powershell",
    ".pl": "perl",
    ".lua": "lua",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
}


def is_probably_text(data: bytes) -> bool:
    """Whether `data` can be scanned as text.

    A NUL byte in the first block is the classic binary tell; beyond that we require the
    bytes to decode as UTF-8, since every scanner downstream works on `str`.
    """
    if b"\x00" in data[:8192]:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


@dataclass(frozen=True)
class SkillFile:
    """One file in the package, with its text if it has any.

    `text` is the raw content of the part we read; `oversized` records that the file
    exceeded the read cap and only a bounded prefix is present, so a payload hidden past
    the cap is still partly scanned and always flagged rather than silently skipped.
    `norm` is the normalised view (invisible/confusable folding, blank-run collapse) that
    the scanners match against; its offset map turns a normalised hit back into a raw span.
    """

    path: str  # POSIX-style, relative to the package root
    size: int
    text: str | None  # None only for binary files; a bounded prefix for oversized ones
    oversized: bool = False

    @property
    def suffix(self) -> str:
        return Path(self.path).suffix.lower()

    @property
    def language_hint(self) -> str:
        """A guess for the labeller's benefit. `unknown` is expected and fine."""
        return _LANGUAGE_HINTS.get(self.suffix, "unknown")

    @property
    def scannable(self) -> bool:
        return self.text is not None

    @cached_property
    def norm(self) -> Normalized:
        """The normalised, offset-mapped view used for matching. Empty for binary files."""
        return normalize(self.text or "")


@dataclass
class SkillPackage:
    """A skill directory, loaded."""

    name: str
    root: Path
    files: list[SkillFile] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, root: Path | str, name: str | None = None) -> SkillPackage:
        root = Path(root).resolve()
        if not root.is_dir():
            raise NotADirectoryError(root)
        pkg = cls(name=name or root.name, root=root)
        total = 0
        for directory, dirs, names in os.walk(root, followlinks=False):
            for name in sorted(dirs):
                if (Path(directory) / name).is_symlink():
                    pkg.issues.append(f"symlink directory skipped: {name}")
            dirs[:] = sorted(n for n in dirs if not (Path(directory) / n).is_symlink())
            for name in sorted(names):
                path = Path(directory) / name
                rel = path.relative_to(root).as_posix()
                if path.is_symlink() or not path.is_file():
                    pkg.issues.append(f"non-regular file skipped: {rel}")
                    continue
                if len(pkg.files) >= 1000 or total >= 32 * MAX_FILE_BYTES:
                    pkg.issues.append("package load cap reached")
                    return pkg
                try:
                    file = _read(path, rel)
                except OSError:
                    pkg.issues.append(f"unreadable file: {rel}")
                    continue
                total += min(file.size, MAX_FILE_BYTES)
                pkg.files.append(file)
                if file.oversized or file.text is None:
                    pkg.issues.append(f"incomplete text coverage: {rel}")
        pkg.files.sort(key=lambda f: f.path)
        return pkg

    @cached_property
    def by_path(self) -> dict[str, SkillFile]:
        return {f.path: f for f in self.files}

    @property
    def entrypoint(self) -> SkillFile | None:
        """The SKILL.md at the package root, if there is one."""
        return self.by_path.get(SKILL_ENTRYPOINT)

    def scannable(self) -> Iterator[SkillFile]:
        """Every file whose text can be scanned, entrypoint first."""
        entry = self.entrypoint
        if entry is not None and entry.scannable:
            yield entry
        for f in self.files:
            if f.scannable and f is not entry:
                yield f

    def resolve(self, source: str, target: str) -> str | None:
        """Resolve a reference in `source` to a package-relative path, or None.

        Returns None for anything that escapes the package — those are recorded by the
        literal scanner as suspicious paths rather than silently followed.
        """
        base = Path(source).parent
        candidate = (base / target) if not target.startswith("/") else Path(target[1:])
        parts: list[str] = []
        for part in candidate.parts:
            if part == "..":
                if not parts:
                    return None
                parts.pop()
            elif part not in (".", ""):
                parts.append(part)
        posix = "/".join(parts)
        return posix if posix in self.by_path else None

    def __len__(self) -> int:
        return len(self.files)


def _read(path: Path, rel: str) -> SkillFile:
    size = path.stat().st_size
    # Always bound the actual read, even if a file grows after stat().
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES)
    text = data.decode("utf-8") if is_probably_text(data) else None
    return SkillFile(path=rel, size=size, text=text, oversized=size > MAX_FILE_BYTES)
