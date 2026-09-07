# Prior work, datasets and competing scanners

Survey done 2026-09-07. Everything below was read directly, not recalled.

## 1. The papers that matter

### Yi Liu et al. — the group whose taxonomy we adopt

| Paper | Venue | What it gives us |
|---|---|---|
| *Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale* ([arXiv 2601.10338](https://arxiv.org/html/2601.10338)) | preprint | The 4-family / 14-pattern taxonomy (`P*`, `E*`, `PE*`, `SC*`). 31,132 skills, 26.1% vulnerable, 5.2% likely malicious. Reported detector: 86.7% precision, 82.5% recall. |
| *"Do Not Mention This to the User": Detecting and Understanding Malicious Agent Skills* ([arXiv 2602.06547](https://arxiv.org/html/2602.06547v3)) | preprint | The **released, MIT-licensed** `MaliciousAgentSkillsBench` — 157 behaviourally-confirmed malicious skills labelled with those 14 patterns, plus a 98,380-skill ecosystem snapshot with download URLs. This is our ground truth. |
| *How Your Credentials Are Leaked by LLM Agent Skills* ([arXiv 2604.03070](https://arxiv.org/html/2604.03070v2)) | **USENIX Security '26** | The credential-specific taxonomy: 4 vulnerability patterns + 6 malicious patterns. 17,022 skills, 520 affected, 1,708 issues. Key finding for us: **76.3% of cases require jointly analysing the natural-language description and the program logic** — i.e. neither a pure NL classifier nor a pure AST pass can see them. That result is the strongest available argument for this project's architecture. |

The credential paper also reports that *information exposure* (stdout captured back into
the agent's context) causes 73.5% of vulnerability issues, and that 89.6% of leaked
credentials are immediately usable.

### Why the composition argument holds

The malicious-skills paper's own case studies are multi-file: the *Flow Nexus* skill
enumerates `~/.ssh` and `~/.aws` in one place and posts to a "analytics" endpoint in
another; the *Email Skill* case pairs a BCC instruction with *"do NOT ask user
permission"* and *"do NOT mention in conversation"*. Single-span scoring sees two boring
sentences. That is the gap the Datalog layer exists to close.

## 2. Datasets

| Dataset | Access | Contents | Use here |
|---|---|---|---|
| [`MaliciousAgentSkillsBench` v0.2](https://zenodo.org/records/20286334) | **open, MIT** | `malicious_skills.csv` (157 confirmed malicious, pattern-labelled, repos anonymised so payloads are *not* included) + `skills_dataset.csv` (98,380 rows: `safe` / `suspicious` / `malicious` with **live download URLs**, redacted only for malicious repos) | Label distribution + ground truth; real `safe` and `suspicious` sample content pulled from the un-redacted URLs |
| [`NVIDIA/SkillSpector` fixtures](https://github.com/NVIDIA/SkillSpector) | Apache-2.0 | ~25 hand-built fixture skills (`tests/fixtures/`) covering semantic injection, NL exfiltration, MCP over-privilege, description/implementation divergence | Vendorable with attribution; good adversarial-but-subtle cases |
| Published PoCs — [Reversec Labs, *Skill Issues* pt.1](https://labs.reversec.com/posts/2026/05/skill-issues-compromising-claude-code-with-malicious-skills-agents-part-1) / [pt.2](https://labs.reversec.com/posts/2026/06/skill-issues-compromising-claude-code-with-malicious-skills-agents-part-2), [Cato CTRL / MedusaLocker](https://www.catonetworks.com/blog/cato-ctrl-weaponizing-claude-skills-with-medusalocker/) | public write-ups | Real working payloads: `allowed-tools: Bash(*)` + `` !`socat ...` `` reverse shell, `GIT_EXTERNAL_DIFF` abuse, `permissionMode: bypassPermissions` npm RCE | Real attack samples, cited, neutralised |
| [`awesome-agent-skills-security`](https://github.com/LLMSecurity/awesome-agent-skills-security) | index | Pointers to InjecAgent, ASB, R-Judge, AgentDojo, SkillCamo, SkillSec-Eval | Future comparison targets; mostly agent-runtime rather than skill-artefact benchmarks |

Note the important gap: nobody publishes the malicious **payloads** openly. The 157
confirmed samples are label-only with anonymised repo ids. So a benchmark that wants real
malicious content has to reconstruct it from published case studies and from the
`suspicious`-labelled skills that *are* downloadable. Our manifest records exactly which
of those a sample is (`provenance` field) so results are never overclaimed.

## 3. Competing scanner: NVIDIA SkillSpector

Apache-2.0, `uv`/`pip`/Docker installable, points at a directory, ZIP, single `SKILL.md`
or git URL. **71 patterns across 17 categories.** Architecture is a LangGraph two-stage
pipeline:

1. **Static** — 11 regex analysers, Python AST behavioural analysis, YARA signatures,
   live OSV.dev CVE lookups, unicode-confusable and whitespace-padding detection.
2. **LLM semantic** — optional, and its stated role is *false-positive filtering* plus
   explanation.

Outputs terminal / JSON / Markdown / SARIF.

Its category set is a superset of the Yi Liu taxonomy — it keeps the same `P1`–`P5`,
`E1`–`E4`, `PE1`–`PE3`, `SC1`–`SC9` identifiers and adds anti-refusal, system-prompt
leakage, memory poisoning, tool misuse, rogue agent, trigger abuse, taint tracking, and
MCP least-privilege / tool-poisoning families.

### Where skillet differs

SkillSpector is a strong, broad **pattern matcher with an LLM as a filter**. The
inversion we are betting on:

- **Direction of the LLM.** They use the LLM to suppress false positives *after* rules
  fire. We use it to *produce* the facts that rules consume, so semantics enter the
  system before the decision instead of after it.
- **Composition.** Their patterns are per-finding. There is no cross-file reachability
  closure, so an attack split across `SKILL.md` and a referenced `reference.md` is two
  low-severity findings rather than one high-severity chain. Datalog transitive closure
  over `Includes` is the whole point of our engine.
- **Auditability.** A pattern hit explains itself as "regex X matched". A Datalog
  derivation explains itself as "rule `exfil_chain` fired on facts `TargetsSensitive(c12)`,
  `Reaches(c12,c31)`, `Egress(c31)`" — each with a file and byte span. That is what makes
  per-rule precision/recall measurable and what lets an analyst overrule one rule without
  disabling a category.
- **Incrementality.** Facts are per-chunk and content-addressed, so a skill update
  re-labels only changed chunks. Their pipeline re-scans.

Where they are ahead and we should not pretend otherwise: OSV.dev CVE lookups, YARA,
SARIF output, and breadth of provider support. SARIF output in particular is cheap for us
to add later and is what makes a scanner usable in CI.

## 4. Threat to the detector itself

The artefact under analysis is adversarial input. Two of the surveyed works attack
scanners directly — *Seeing Is Not Screening* ([arXiv 2606.18198](https://arxiv.org/pdf/2606.18198))
demonstrates multimodal hidden-instruction attacks against skill scanners, and SkillSpector
ships whitespace-padding and unicode-confusable detectors precisely because reviewers
never see what the agent reads.

Consequences for our design, enforced in `CLAUDE.md`:
chunks are passed as delimited data with an explicit "sample to be labelled, not
instructions" framing; the labeller is given no tools; each chunk is labelled
independently; the model never sees the rule set; and off-schema output is dropped rather
than repaired.
