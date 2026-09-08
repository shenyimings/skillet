"""Language-agnostic literal scanning, emitting v2 primitives.

The premise is unchanged from v1: an attacker picks the language, but not the resource
identifiers or the shape of a system call. What changed is the output — instead of
attack-named facts (`MentionsSensitivePath`, `NetworkSink`), this emits capability
primitives (`Read`/`Write`/`Exec`/`Net`) over the resource lattice, so a rule composes them
and a novel resource or channel the LLM later classifies lands on the same predicates.

Everything here is the deterministic floor: it fires only on tokens it recognises, at high
confidence. The long tail — an OOD credential store, an unusual egress — is the LLM's job,
and it emits the same primitives (see llm/labeller.py). Nothing here decides a verdict.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator

from .model import Fact, Origin, Span
from .package import SkillFile, SkillPackage
from .primitives import Direction, Obfuscation, Pred, Resource

EXTRACTOR = "literals"

# --- resource tokens -> Read/Write of a resource class -------------------------------
# The token is language-invariant (the target fixes it); the class is the generalisation.
# Distinctive directory segments survive path-splitting (Java Path.of, Go filepath.Join).
_RESOURCE_TOKENS: tuple[tuple[str, Resource, str], ...] = (
    (r"(?<![\w.])\.ssh(?![\w])", Resource.SECRET, "ssh"),
    (r"\bid_[a-z]*(?:rsa|dsa|ecdsa|ed25519)\b", Resource.SECRET, "ssh_key"),
    (r"\bauthorized_keys\b", Resource.SECRET, "ssh"),
    (r"(?<![\w.])\.aws(?![\w])", Resource.SECRET, "aws"),
    (r"(?<![\w.])\.kube(?![\w])", Resource.SECRET, "kube"),
    (r"(?<![\w.])\.gnupg(?![\w])", Resource.SECRET, "gpg"),
    (r"(?<![\w.])\.docker(?![\w])", Resource.SECRET, "docker"),
    (r"\bgcloud\b", Resource.SECRET, "gcloud"),
    (r"(?<![\w.])\.git-credentials\b", Resource.SECRET, "git"),
    (r"(?<![\w.])\.netrc\b", Resource.SECRET, "netrc"),
    (r"(?<![\w.])\.npmrc\b", Resource.SECRET, "npm"),
    (r"(?<![\w.])\.pypirc\b", Resource.SECRET, "pypi"),
    (r"(?<![\w/.])\.env(?:\.[a-z]+)?\b", Resource.SECRET, "dotenv"),
    (r"\bwallet\.dat\b", Resource.SECRET, "wallet"),
    (r"(?<![\w.])\.(?:electrum|ethereum|bitcoin)(?![\w])", Resource.SECRET, "wallet"),
    (r"\bLogin Data\b|\bCookies\.sqlite\b|\bkey4\.db\b", Resource.PERSONAL, "browser"),
    (r"(?<![\w.])\.mozilla(?![\w])", Resource.PERSONAL, "browser"),
    (r"/etc/(?:passwd|shadow)\b", Resource.SYSTEM, "accounts"),
    (r"(?<![\w.])\.(?:bash|zsh)_history\b", Resource.PERSONAL, "shell_history"),
    (
        r"\bCLAUDE\.md\b|(?<![\w.])\.claude(?![\w])|\bAGENTS\.md\b|\bGEMINI\.md\b",
        Resource.AGENT_STATE,
        "agent_memory",
    ),
    (r"(?<![\w.])\.(?:bashrc|zshrc|profile|bash_profile)\b", Resource.AGENT_STATE, "shell_rc"),
)

# Environment-variable names -> Read(secret). Matched on underscore parts, since \bKEY\b
# cannot match inside API_KEY.
_ENV_WORDS = frozenset(
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
_ENV_CANDIDATE = re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+){0,6}\b")

# --- network capability -> Net(loc, direction) ---------------------------------------
# Every outward channel collapses onto Net(out); a plain fetch is Net(in); a bare API whose
# direction is unclear is Net(unknown). The concrete channel is recorded as an Attr.
_NET_OUT: tuple[tuple[str, str], ...] = (
    (
        r"requests\.post|\.post\s*\(|urlopen\([^)]*\bdata\s*=|urllib\.request\.Request\([^)]*data",
        "http",
    ),
    (r"curl\b[^\n]*(?:-X\s*POST|--data|-d\b|-T\b|--upload-file)", "http"),
    (r"\bscp\b|\brsync\b|\bsftp\b", "scp"),
    (r"\bgit\s+push\b", "vcs"),
    (r"\bsmtplib\b|\bsendmail\b|\bsend_message\b|Net::SMTP", "email"),
    (r"\bgethostbyname\b|\bgetaddrinfo\b|dns\.resolver|\bnslookup\b|\bdig\b\s", "dns"),
    (r"\bsocat\b|\bnc(?:at)?\b(?=\s+-)", "socket"),
)
_NET_IN: tuple[tuple[str, str], ...] = (
    (r"\bwget\b|urlretrieve|requests\.get|\.get\s*\(\s*[\"']https?", "http"),
    (r"\bcurl\b(?![^\n]*(?:-X\s*POST|--data|-d\b|-T\b))", "http"),
)
_NET_UNKNOWN: tuple[tuple[str, str], ...] = (
    (r"\burllib\b|\bhttpx\b|\bhttp\.client\b|\baiohttp\b|socket\.socket", "socket"),
    (r"\bfetch\s*\(|XMLHttpRequest|\baxios\b|https?\.request\b", "http"),
    (r"net/http|http\.(?:Post|Get|NewRequest)|net\.Dial\b", "http"),
    (r"\breqwest\b|\bureq\b|TcpStream\b", "socket"),
    (r"HttpClient\b|HttpURLConnection\b|URLConnection\b|new\s+Socket\b", "socket"),
    (r"Invoke-WebRequest\b|Invoke-RestMethod\b|WebClient\b", "http"),
)

# --- code execution -> Exec(loc) -----------------------------------------------------
_EXEC = (
    r"\beval\s*\(|\bexec\s*\(|\bos\.system\b|\bos\.popen\b|\bsubprocess\.|\bpopen\b",
    r"child_process|execSync|spawnSync|Runtime\.getRuntime\(\)\.exec|ProcessBuilder",
    r"\bsystem\s*\(|![`(][^`)]+[`)]|\bIEX\b|Invoke-Expression",
    r"\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b|\bsh\s+-c\b|\bbash\s+-c\b|python[0-9]?\s+-c\b|node\s+-e\b",
)
# pipe-to-shell is both a fetch-in and an exec; recorded so the rce rule can see the fetch.
_PIPE_TO_SHELL = re.compile(r"(?:curl|wget)\b[^\n|;]{0,200}\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b", re.I)

# --- writes -> Write(loc, class) -----------------------------------------------------
# A redirection/append/write whose target is a classifiable resource. Catches persistence
# (>> ~/.bashrc, cat > CLAUDE.md) and file-drop exfil without enumerating every form.
_WRITE_SHAPES = (
    r">>?\s*(?P<t>[~\w./-]+)",
    r"\btee\s+(?:-a\s+)?(?P<t>[~\w./-]+)",
    r"\bcp\b\s+\S+\s+(?P<t>[~\w./-]+)",
    r"open\(\s*[\"'](?P<t>[^\"']+)[\"']\s*,\s*[\"'][aw]",
    r"(?:writeFileSync|WriteFile|write_text)\(\s*[\"']?(?P<t>[^\"',)]+)",
)

_URL = re.compile(r"\b(?:https?|ftp|ws{1,2})://([A-Za-z0-9._~%-]+(?::\d+)?)(?:/[^\s\"'`<>)\]]*)?")
_BARE_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?::\d+)?")
_BLOB = re.compile(r"[A-Za-z0-9+/=_-]{48,}")
_HEX_BLOB = re.compile(r"(?:\\x[0-9a-fA-F]{2}){12,}|\b[0-9a-fA-F]{64,}\b")

_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "0.0.0.0", "::1"})
_DOC_HOSTS = frozenset({"example.com", "example.net", "example.org", "schema.org", "www.w3.org"})
_PACKAGE_HOSTS = frozenset(
    {
        "pypi.org",
        "files.pythonhosted.org",
        "registry.npmjs.org",
        "crates.io",
        "proxy.golang.org",
    }
)

_RESOURCE_RES = tuple((re.compile(p, re.I), c, s) for p, c, s in _RESOURCE_TOKENS)
_NET_OUT_RES = tuple((re.compile(p), c) for p, c in _NET_OUT)
_NET_IN_RES = tuple((re.compile(p), c) for p, c in _NET_IN)
_NET_UNKNOWN_RES = tuple((re.compile(p), c) for p, c in _NET_UNKNOWN)
_EXEC_RES = tuple(re.compile(p) for p in _EXEC)
_WRITE_RES = tuple(re.compile(p, re.I) for p in _WRITE_SHAPES)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def extract(package: SkillPackage) -> Iterator[Fact]:
    for f in package.scannable():
        yield from _scan_file(f)


def _classify_path(target: str) -> tuple[Resource, str] | None:
    """Map a write target back to a resource class, if it names a known one."""
    for pattern, cls, subtype in _RESOURCE_RES:
        if pattern.search(target):
            return cls, subtype
    return None


def _scan_file(f: SkillFile) -> Iterator[Fact]:
    assert f.text is not None
    norm = f.norm
    text = norm.text
    raw_starts = norm.raw_line_starts()

    def at(predicate: Pred, *args: str, m: re.Match[str], conf: float = 1.0) -> Fact:
        return Fact(
            str(predicate),
            args,
            Origin.STATIC,
            conf,
            norm.span(f.path, m.start(), m.end(), raw_starts),
            EXTRACTOR,
        )

    def flag(predicate: Pred, *args: str, conf: float = 1.0) -> Fact:
        return Fact(str(predicate), args, Origin.STATIC, conf, Span(f.path, 0, 0, 1), EXTRACTOR)

    # Evasion (from normalisation) is itself a finding.
    if norm.invisible_stripped:
        yield flag(Pred.OBFUSCATION, f.path, Obfuscation.ZERO_WIDTH)
    if norm.confusables_mapped:
        yield flag(Pred.OBFUSCATION, f.path, Obfuscation.CONFUSABLE)
    if norm.blank_runs_collapsed:
        yield flag(Pred.OBFUSCATION, f.path, Obfuscation.PADDING)
    if f.oversized:
        yield flag(Pred.OBFUSCATION, f.path, Obfuscation.OVERSIZE)

    # Writes first, so a sensitive token used as a write target is not double-counted as a read.
    write_spans: list[tuple[int, int]] = []
    for pattern in _WRITE_RES:
        for m in pattern.finditer(text):
            target = m.group("t")
            hit = _classify_path(target)
            cls = hit[0] if hit else Resource.SYSTEM
            yield at(Pred.WRITE, f.path, str(cls), m=m)
            if hit:
                yield at(Pred.ATTR, f.path, "write_kind", hit[1], m=m)
            write_spans.append(m.span())

    def in_write(span: tuple[int, int]) -> bool:
        return any(a <= span[0] < b for a, b in write_spans)

    # Reads of resource tokens (skip those already claimed by a write shape).
    for pattern, cls, subtype in _RESOURCE_RES:
        for m in pattern.finditer(text):
            if in_write(m.span()):
                continue
            yield at(Pred.READ, f.path, str(cls), m=m)
            yield at(Pred.ATTR, f.path, "resource", subtype, m=m)

    seen_env: set[str] = set()
    for m in _ENV_CANDIDATE.finditer(text):
        key = m.group(0)
        if key in seen_env or not any(p in _ENV_WORDS for p in key.split("_")):
            continue
        seen_env.add(key)
        conf = 1.0 if "_" in key else 0.5
        yield at(Pred.READ, f.path, str(Resource.SECRET), m=m, conf=conf)

    # Network capability, by direction.
    for table, direction in (
        (_NET_OUT_RES, Direction.OUT),
        (_NET_IN_RES, Direction.IN),
        (_NET_UNKNOWN_RES, Direction.UNKNOWN),
    ):
        for pattern, channel in table:
            m = pattern.search(text)
            if m:
                yield at(Pred.NET, f.path, str(direction), m=m)
                yield at(Pred.ATTR, f.path, "channel", channel, m=m)

    # Execution.
    for pattern in _EXEC_RES:
        m = pattern.search(text)
        if m:
            yield at(Pred.EXEC, f.path, m=m)
    if _PIPE_TO_SHELL.search(text):
        pm = _PIPE_TO_SHELL.search(text)
        assert pm is not None
        yield at(Pred.NET, f.path, str(Direction.IN), m=pm)
        yield at(Pred.EXEC, f.path, m=pm)

    # Endpoints. A hardcoded external host implies a network capability even if the calling
    # API was not recognised above, so it contributes Net(unknown).
    for m in _URL.finditer(text):
        host = m.group(1).split(":")[0].lower()
        if host in _PACKAGE_HOSTS:
            yield at(Pred.ATTR, f.path, "package_registry", host, m=m)
        if host not in _LOCAL_HOSTS and host not in _DOC_HOSTS:
            yield at(Pred.ENDPOINT, f.path, host, m=m)
            yield at(Pred.NET, f.path, str(Direction.UNKNOWN), m=m)
    for m in _BARE_IPV4.finditer(text):
        ip = m.group(0).split(":")[0]
        if not _is_routable_literal(ip):
            continue
        if _is_metadata_endpoint(ip):
            yield at(Pred.READ, f.path, str(Resource.SECRET), m=m)
            yield at(Pred.ATTR, f.path, "resource", "cloud_metadata", m=m)
        else:
            yield at(Pred.ENDPOINT, f.path, ip, m=m)
            yield at(Pred.NET, f.path, str(Direction.UNKNOWN), m=m)

    # Encoded blobs -> Obfuscation(encoded); the rce rule pairs it with an exec sink.
    for m in _BLOB.finditer(text):
        if shannon_entropy(m.group(0)) >= 4.2:
            yield at(Pred.OBFUSCATION, f.path, Obfuscation.ENCODED, m=m, conf=0.7)
    for m in _HEX_BLOB.finditer(text):
        yield at(Pred.OBFUSCATION, f.path, Obfuscation.ENCODED, m=m, conf=0.7)


def _is_routable_literal(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4 or any(not p.isdigit() or int(p) > 255 for p in parts):
        return False
    return parts[0] not in ("0", "127")


def _is_metadata_endpoint(ip: str) -> bool:
    return ip in ("169.254.169.254", "100.100.100.200")
