# v2: a primitive fact vocabulary

## The problem with v1

v1's predicates were read off the benchmark: `MentionsSensitivePath(f, "aws_credentials")`,
`NetworkSink(f, "python")`, one entry per attack seen. That is a denylist wearing a
predicate's clothes. It does not generalise: a credential store not in the table, an
egress channel not in the list (DNS, `git push`, `scp`), or a novel phrasing produces *no
fact*, so no rule can fire. Red-team round 2 proved it — 4 of 6 bypasses were simply
"a verb or resource skillet hadn't enumerated".

## The v2 idea: a small capability / information-flow calculus

Almost every skill attack is some composition of a handful of **primitive verbs over a
small lattice of resource classes**, connected by **information flow**. So the fact
vocabulary should be those primitives — not the attacks. New attacks are then *expressed*
in the existing vocabulary rather than requiring a new predicate.

Both tiers populate the *same* primitives:

- **static** maps known tokens to primitives — precise, high confidence, the language-
  agnostic floor;
- **the LLM** maps *anything* to the same primitives — it classifies an out-of-distribution
  resource into the lattice, recognises an unusual egress as an outward send, and asserts
  **Flow** between points when it can see the dataflow. This is where the LLM finally earns
  its place: it covers the long tail static can't enumerate, speaking the same language the
  rules consume.

### Verbs (the "instruction set")

`loc` is a chunk id or a file path. Every fact carries origin + confidence + span as before.

| predicate | meaning |
|---|---|
| `Read(loc, class)` | reads a resource of the given class |
| `Write(loc, class)` | creates or modifies a resource of the given class |
| `Exec(loc)` | runs code / spawns a process / evaluates a payload |
| `Net(loc, dir)` | communicates over *any* channel; `dir` ∈ `out` / `in` / `unknown`. **Outward movement of every kind maps here** — http, DNS, `scp`, `git push`, email, a shared-drive write — so the exfil rule needs one predicate, not one per channel. The concrete channel rides along as an `Attr`. |
| `Flow(a, b)` | information or control flows from `a` to `b` (taint / reachability) |
| `Directive(loc)` | the text instructs the agent to do something |
| `Claim(loc, kind)` | a framing claim; `kind` ∈ `authority` / `conceal` / `persist` / `deceive` |
| `Declares(skill, cap)` | a frontmatter-declared capability grant; `cap` ∈ `wildcard` / `unattended` / a tool name |

### Resource lattice (`class`)

Deliberately few and categorical, so a novel resource still lands somewhere:

| class | examples (static seeds; LLM extends) |
|---|---|
| `secret` | credentials, API keys, SSH/GPG keys, tokens, passwords, cloud-metadata |
| `personal` | user PII, conversation/context, browser data |
| `agent_state` | `CLAUDE.md`, `.claude/`, agent memory/config |
| `code` | scripts, dependencies, an interpreter's input |
| `system` | environment variables, arbitrary/system files, process state |

### Evidence / attributes (keep detail without exploding the predicate count)

| predicate | meaning |
|---|---|
| `Endpoint(loc, host)` | a concrete external destination literal (provenance for a `Net`) |
| `Obfuscation(loc, kind)` | `confusable` / `zero_width` / `padding` / `oversize` / `encoded` |
| `Attr(loc, key, value)` | open side-channel, e.g. `Attr(l,"channel","dns")`, `Attr(l,"secret_kind","aws")` |
| `CoInSkill(a, b)` | `a` and `b` are both in the same package (weak reachability, no edge) |

### Structural (unchanged)

`InFile(loc, file)`, `Includes(file, file)`, `File(skill, file, lang)`.

## Rules become general (and few)

```
# reachability
Flow(A,B) :- InFile(A,F), InFile(B,F).                       # same file (strong)
Flow(A,B) :- InFile(A,F1), Includes(F1,F2), InFile(B,F2).    # via an include edge
Flow(A,C) :- Flow(A,B), Flow(B,C).                           # transitive

# exfiltration: a sensitive read reaches an outward send — ANY channel
exfiltration      :- Read(A, secret|personal), Flow(A,B), Net(B, out)      # HIGH
exfiltration_weak :- Read(A, secret|personal), CoInSkill(A,B), Net(B, out) # MEDIUM (no edge)

# remote code execution / reverse shell
rce           :- Net(A,_), Flow(A,B), Exec(B)     # fetch-then-run
reverse_shell :- Exec(A), Flow(A,B), Net(B, out)  # spawn a shell wired outward
exec_obfusc   :- Exec(A), Obfuscation(A, encoded) # run a decoded blob

# prompt injection / manipulation
injection  :- Claim(A, authority), Flow(A,B), Claim(B, conceal)  # dominate + hide
conceal    :- Claim(A, conceal)                                  # "do not tell the user"
deception  :- Claim(A, deceive), Directive(A)

# persistence
persistence :- Write(A, agent_state)
persistence :- Claim(A, persist)

# over-privilege
overprivilege :- Declares(S, wildcard)
overprivilege :- Declares(S, unattended)

# the evasion attempt is itself the finding
evasion :- Obfuscation(A, confusable|zero_width|padding|oversize)
```

Note what this buys, measured against the round-2 bypasses:

- **DNS exfil, `git push` exfil, `scp` exfil** all become `Read(secret) → Flow → Net(out)`
  — one rule, because every outward channel is `Net(out)`.
- **A credential store not in any table** becomes `Read(_, secret)` the moment the LLM (or a
  broadened static heuristic) classifies it — the rule is unchanged.
- **The reverse-shell gap** (socat + external host) is now `Exec ∧ Flow ∧ Net(out)`.
- **Cross-file split injection** is `Claim(authority) → Flow → Claim(conceal)` over the
  include/`CoInSkill` graph.

## What stays

The engine (semi-naive Datalog + provenance + confidence-as-min), the chunker, the
normaliser, the package loader, the DSL compiler, the benchmark and evaluator — all
unchanged. v2 is a vocabulary change: new `facts/primitives.py`, extractors re-pointed to
emit primitives, `core.skl` rewritten, the LLM schema re-pointed to primitives + `Flow`.
The anti-injection posture is untouched: the LLM still emits only schema facts, one chunk
at a time, no verdict, no rule set.
