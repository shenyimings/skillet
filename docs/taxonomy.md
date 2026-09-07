# Classification scheme

## Which taxonomy, and why

The user asked for the Yi Liu et al. USENIX Security '26 scheme. That group published two
overlapping taxonomies, and they serve different purposes, so the benchmark carries both:

**Primary axis — 4 families / 14 patterns.** This is the taxonomy from *Agent Skills in
the Wild*, and crucially it is the label set actually applied to the 157
behaviourally-confirmed malicious skills in their released `MaliciousAgentSkillsBench`.
Labelling against it means our per-class counts are directly comparable to their ground
truth, and the pattern identifiers (`P1`–`P4`, `E1`–`E4`, `PE1`–`PE3`, `SC1`–`SC3`) are
the same ones NVIDIA SkillSpector reports, so cross-tool comparison is free.

**Secondary axis — credential-leakage patterns.** The USENIX '26 paper proper
(*How Your Credentials Are Leaked by LLM Agent Skills*) is credential-specific: 4
vulnerability patterns and 6 malicious patterns. It is a finer lens on one slice rather
than a replacement, and it distinguishes *negligent* from *hostile* in a way the primary
axis does not. Samples that involve credentials carry a `credential_pattern` label too.

A sample may carry several primary patterns; that is normal, and the real data shows it —
in the 157 confirmed malicious skills the mean is ~3 patterns per skill, with
`Remote Code Execution` (118), `Network sniffing / Credential theft` (101) and
`Behavior Manipulation` (100) the most common.

## Primary axis

### PI — Prompt Injection
Instructions aimed at the *agent* rather than at the user's task.

| ID | Name | Definition |
|---|---|---|
| `P1` | Instruction Override | Explicit commands to ignore user or system constraints. |
| `P2` | Hidden Instructions | Directives concealed from human review — HTML comments, zero-width or confusable characters, whitespace padding that pushes text off-screen, text the agent reads but the reviewer does not. |
| `P3` | Context Leakage | Instructions directing the agent to transmit conversation context, user data or system prompt outward. |
| `P4` | Behavior Manipulation | Subtle steering of agent decision-making — preference injection, silent defaults, suppression of disclosure ("do not mention this to the user"). |

### EX — Data Exfiltration
Movement of sensitive data out of the user's environment.

| ID | Name | Definition |
|---|---|---|
| `E1` | External Transmission | Sending collected data to a hardcoded external endpoint. |
| `E2` | Credential Harvesting | Enumerating environment variables, keyrings or network traffic for secrets. (The released labels call this *Network sniffing / Credential theft*.) |
| `E3` | File System Scan | Enumerating directories for sensitive files — `~/.ssh`, `~/.aws`, `~/.config`, wallet files, browser stores. |
| `E4` | Context Exfiltration | Transmitting agent conversation context to an external service. Distinguished from `P3` by layer: `P3` is the *instruction*, `E4` is the *code or endpoint* that carries it out. |

### PE — Privilege Escalation

| ID | Name | Definition |
|---|---|---|
| `PE1` | Excessive Permissions | Requested scope exceeds stated functionality — broad `allowed-tools`, `permissionMode: bypassPermissions`. |
| `PE2` | Sudo / Root Execution | Elevated privileges invoked without justification. |
| `PE3` | Credential Access | Reading authentication tokens, key files or password stores; also hardcoded tokens shipped inside the skill. |

### SC — Supply Chain

| ID | Name | Definition |
|---|---|---|
| `SC1` | Unpinned Dependencies | No version constraint, so a later malicious release is silently adopted. |
| `SC2` | Remote Code Execution | Code fetched from a remote URL and executed at runtime — `curl \| sh`, dynamic import, alternate package registry. |
| `SC3` | Code Obfuscation | Deliberately obscured logic: base64/hex payloads with an execution sink, encoding chains, dead-drop resolvers. |

## Secondary axis — credential leakage (USENIX Sec '26)

Split by intent, which is the distinction that matters for triage: the first four are
mistakes, the last six are attacks.

**Vulnerability patterns** (negligence)

| ID | Name | Definition |
|---|---|---|
| `CV1` | Hardcoded Credentials | Secrets as string literals in code, docs or config. |
| `CV2` | Insecure Storage | Credentials passed via CLI arguments, process parameters or URL parameters. |
| `CV3` | Information Exposure | Console logs, debug output or API responses whose stdout is captured back into the agent's context. **73.5% of observed issues.** |
| `CV4` | Artifact Leakage | Credentials persisted into shell history, temp files, cache or git config. |

**Malicious patterns** (intent)

| ID | Name | Definition |
|---|---|---|
| `CM1` | Remote Exploitation | RCE backdoors, reverse shells, persistent control channels. |
| `CM2` | Defense Evasion | Encoding or obfuscation aimed at bypassing detection. |
| `CM3` | Credential Compromise | Theft of environment variables or SSH keys, including by social engineering the user. |
| `CM4` | Data Exfiltration | Keyloggers, webhook harvesting, XSS. |
| `CM5` | Resource Hijacking | Cryptominers and other resource theft. |
| `CM6` | Persistence | C2 beaconing, authorized-key deployment, writes to `CLAUDE.md` or agent memory. |

## Verdict labels

Following the released dataset's three-way split:

- `benign` — no finding expected. A detector alerting here is a false positive.
- `suspicious` — genuinely risky capability without confirmed hostile intent
  (over-broad permissions, unpinned deps, debug logging of secrets). Severity `LOW`/`MEDIUM`.
- `malicious` — confirmed hostile intent. Severity `HIGH`/`CRITICAL`.

`suspicious` is deliberately kept as its own class rather than folded into either side.
It is where scanners actually differ, and averaging it away hides the interesting errors.

## Cross-mapping

The `benchmark/schema/taxonomy.yaml` file is the machine-readable form and is what the
manifest validates against. It carries, per pattern, the `skillspector_id` (identical for
the 14 primary patterns) so comparative evaluation needs no translation table.
