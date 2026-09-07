"""Language-agnostic literal scanning — the floor that no language switch can drop below.

The premise: an attacker picks the language, but not the *resource identifiers*. Reading
an AWS key means naming `~/.aws/credentials` whether the code is Python, Go, Rust or Java;
exfiltrating means writing the endpoint down; harvesting means naming the environment
variable. Those strings are dictated by the target, so a scanner that keys on them is
invariant to how the surrounding program is written.

So this module reads every scannable file as flat text and emits facts about the
identifiers it names. It does not know or care what language it is looking at, and it runs
before — and independently of — any parser. Everything a language-specific extractor adds
later is confidence, never coverage.

What this deliberately does *not* do is decide anything. `MentionsCommand(f, "curl")` is
not an accusation; plenty of honest skills call curl. Composition is the engine's job.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator

from .model import Fact, Origin, Span, line_of, line_starts
from .package import SkillFile, SkillPackage

EXTRACTOR = "literals"

# --- Resource identifier tables ------------------------------------------------------
# These are the language-invariant part of an attack. Each entry names a resource whose
# location the *target* fixes, so it reads identically in every implementation language.

_SENSITIVE_PATHS: tuple[tuple[str, str], ...] = (
    # Distinctive directory segments — the anchor, present however the path is assembled.
    (r"(?<![\w.])\.ssh(?![\w])", "ssh_dir"),
    (r"(?<![\w.])\.aws(?![\w])", "aws_credentials"),
    (r"(?<![\w.])\.kube(?![\w])", "kube_config"),
    (r"(?<![\w.])\.gnupg(?![\w])", "gpg_keys"),
    (r"(?<![\w.])\.docker(?![\w])", "docker_config"),
    (r"\bgcloud\b", "gcloud_config"),
    (r"(?<![\w.])\.mozilla(?![\w])", "browser_store"),
    # Distinctive filenames — unambiguous on their own, so a split path still trips them.
    (r"\bid_[a-z]*(?:rsa|dsa|ecdsa|ed25519)\b", "ssh_private_key"),
    (r"\bauthorized_keys\b", "ssh_authorized_keys"),
    (r"(?<![\w.])\.git-credentials\b", "git_credentials"),
    (r"(?<![\w.])\.netrc\b", "netrc"),
    (r"(?<![\w.])\.npmrc\b", "npmrc"),
    (r"(?<![\w.])\.pypirc\b", "pypirc"),
    (r"\bwallet\.dat\b", "crypto_wallet"),
    (r"(?<![\w.])\.(?:electrum|ethereum|bitcoin)(?![\w])", "crypto_wallet"),
    (r"\bLogin Data\b|\bCookies\.sqlite\b|\bkey4\.db\b", "browser_store"),
    (r"/etc/(?:passwd|shadow)\b", "system_accounts"),
    (r"(?<![\w.])\.(?:bash|zsh)_history\b", "shell_history"),
    (r"(?<![\w/.])\.env(?:\.[a-z]+)?\b", "dotenv"),
    # Agent-state files: writing to these is how a skill makes itself persistent.
    (r"\bCLAUDE\.md\b|(?<![\w.])\.claude(?![\w])|\bAGENTS\.md\b|\bGEMINI\.md\b", "agent_memory"),
)

# Environment variable names. Matching is on underscore-separated parts rather than with
# word boundaries, because `\bKEY\b` cannot match inside `API_KEY` — `_` is a word
# character, so the boundary never appears and every underscored name would be missed.
_ENV_KEY_WORDS = frozenset(
    {
        "KEY",
        "KEYS",
        "APIKEY",
        "SECRET",
        "SECRETS",
        "TOKEN",
        "TOKENS",
        "PASSWORD",
        "PASSWD",
        "PASS",
        "CREDENTIAL",
        "CREDENTIALS",
        "CREDS",
        "AUTH",
        "PRIVATE",
        "SESSION",
        "COOKIE",
        "SIGNATURE",
    }
)
_ENV_KEY_CANDIDATE = re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+){0,6}\b")

# Commands whose presence is worth recording. Not a blocklist — a fact, not a verdict.
_COMMANDS: tuple[tuple[str, str], ...] = (
    (r"\bcurl\b", "curl"),
    (r"\bwget\b", "wget"),
    (r"\bsocat\b", "socat"),
    (r"\bnc(?:at)?\b(?=\s+-)", "netcat"),
    (r"\bsudo\b", "sudo"),
    (r"\bdoas\b", "doas"),
    (r"\bchmod\s+\+?x\b|\bchmod\s+[0-7]{3,4}\b", "chmod"),
    (r"\bbase64\s+(?:-d|--decode)\b", "base64_decode"),
    (r"\bcertutil\b", "certutil"),
    (r"\bpowershell\b|\bIEX\b", "powershell"),
    (r"\bcrontab\b", "crontab"),
    (r"\bsystemctl\b", "systemctl"),
    (r"\bxxd\b|\bod\s+-", "hexdump"),
    (r"\bnohup\b|\bdisown\b|\bsetsid\b", "detach"),
    (r"\bgit\s+config\b", "git_config"),
)

# `curl … | sh` and friends: the pipe-to-shell shape survives every language because it is
# a shell construct regardless of what invokes it.
_PIPE_TO_SHELL = re.compile(r"(?:curl|wget)\b[^\n|;]{0,200}\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b", re.I)

_URL = re.compile(r"\b(?:https?|ftp|ws{1,2})://([A-Za-z0-9._~%-]+(?::\d+)?)(?:/[^\s\"'`<>)\]]*)?")
_BARE_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?::\d+)?")
# Long unbroken run of base64/hex alphabet — an encoded payload looks the same everywhere.
_BLOB = re.compile(r"[A-Za-z0-9+/=_-]{48,}")
_HEX_BLOB = re.compile(r"(?:\\x[0-9a-fA-F]{2}){12,}|\b[0-9a-fA-F]{64,}\b")

# Hosts that are noise: documentation ranges, package registries, the user's own machine.
_UNREMARKABLE_HOSTS = frozenset(
    {
        "localhost",
        "example.com",
        "example.net",
        "example.org",
        "github.com",
        "raw.githubusercontent.com",
        "pypi.org",
        "files.pythonhosted.org",
        "registry.npmjs.org",
        "crates.io",
        "proxy.golang.org",
        "schema.org",
        "www.w3.org",
    }
)

_SENSITIVE_PATH_RES = tuple((re.compile(p, re.I), kind) for p, kind in _SENSITIVE_PATHS)
_COMMAND_RES = tuple((re.compile(p, re.I), name) for p, name in _COMMANDS)


def shannon_entropy(s: str) -> float:
    """Bits per character. Encoded payloads sit high; English prose and code sit low."""
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def extract(package: SkillPackage) -> Iterator[Fact]:
    """Emit language-agnostic literal facts for every scannable file in `package`."""
    for f in package.scannable():
        yield from _scan_file(f)


def _scan_file(f: SkillFile) -> Iterator[Fact]:
    text = f.text
    assert text is not None  # guaranteed by SkillPackage.scannable()
    starts = line_starts(text)

    def fact(predicate: str, *args: str, at: re.Match[str], confidence: float = 1.0) -> Fact:
        return Fact(
            predicate=predicate,
            args=args,
            origin=Origin.STATIC,
            confidence=confidence,
            span=Span(f.path, at.start(), at.end(), line_of(starts, at.start())),
            extractor=EXTRACTOR,
        )

    for m in _URL.finditer(text):
        host = m.group(1).split(":")[0].lower()
        yield fact("MentionsHost", f.path, host, at=m)
        if host not in _UNREMARKABLE_HOSTS:
            yield fact("MentionsExternalHost", f.path, host, at=m)

    for m in _BARE_IPV4.finditer(text):
        ip = m.group(0).split(":")[0]
        if _is_routable_literal(ip):
            yield fact("MentionsHost", f.path, ip, at=m)
            yield fact("MentionsExternalHost", f.path, ip, at=m)

    for pattern, kind in _SENSITIVE_PATH_RES:
        for m in pattern.finditer(text):
            yield fact("MentionsSensitivePath", f.path, kind, at=m)

    for pattern, name in _COMMAND_RES:
        for m in pattern.finditer(text):
            yield fact("MentionsCommand", f.path, name, at=m)

    for m in _PIPE_TO_SHELL.finditer(text):
        yield fact("PipesToShell", f.path, at=m)

    seen_env: set[str] = set()
    for m in _ENV_KEY_CANDIDATE.finditer(text):
        key = m.group(0)
        if key in seen_env:
            continue
        parts = key.split("_")
        if not any(p in _ENV_KEY_WORDS for p in parts):
            continue
        seen_env.add(key)
        # A qualified name (`AWS_SECRET_ACCESS_KEY`) is almost certainly an env var; a bare
        # `TOKEN` in prose often is not, so it is asserted more weakly rather than dropped.
        yield fact("MentionsEnvKey", f.path, key, at=m, confidence=1.0 if len(parts) > 1 else 0.5)

    for m in _BLOB.finditer(text):
        blob = m.group(0)
        # Entropy separates an encoded payload from a long identifier or a hash-like token.
        if shannon_entropy(blob) >= 4.2:
            yield fact("OpaqueBlob", f.path, "base64", at=m, confidence=0.7)

    for m in _HEX_BLOB.finditer(text):
        yield fact("OpaqueBlob", f.path, "hex", at=m, confidence=0.7)


def _is_routable_literal(ip: str) -> bool:
    """Filter version strings and loopback; keep addresses that could be a real endpoint."""
    parts = ip.split(".")
    if len(parts) != 4 or any(not p.isdigit() or int(p) > 255 for p in parts):
        return False
    return parts[0] not in ("0", "127")
