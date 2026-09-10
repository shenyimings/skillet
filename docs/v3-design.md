# V3: static facts, selective Pi review, external state

V3 replaces the default per-chunk labelling pipeline. It uses the actual
[`@earendil-works/pi-agent-core`](https://github.com/earendil-works/pi) runtime,
pinned to 0.85.1 with `pi-ai` and a committed npm lockfile. It does not launch the
coding-agent CLI or give it default shell/filesystem tools.

The [RLM design](https://alexzhang13.github.io/blog/2025/rlm/) motivates keeping the
long source outside model context and inspecting it selectively. This is **RLM-inspired
retrieval, not an implementation of the paper's recursive REPL**. No recursive LLM calls
or LLM-based compaction are used. RLM alone is not a state-management scheme.

## Execution

1. Python loads a bounded snapshot. Symlinks, nonregular files and oversized/binary
   content produce explicit coverage issues. Maximum 1 MiB per file, 1,000 files and
   32 MiB total loaded prefixes. No sample code runs.
2. Static frontmatter/include/literal facts become source-specific event nodes. Python
   AST adds narrowly supported direct assignment-to-HTTP-payload dataflow, including
   import aliases and reassignment kills. Other languages keep lexical evidence.
3. Pi starts with instructions and host counts, not a concatenation of source chunks.
   It pages file metadata, facts and gaps, reads relevant prose, and reviews code only
   through a named static-review gap. File IDs resolve only against the snapshot.
4. Exact quotations from previously issued source handles admit closed-schema facts.
   Edges require existing endpoints, reads covering both endpoint spans, and anchored
   relationship evidence. The host records accepted/rejected decisions. An agent cannot
   erase static confirmed edges or emit an alert.
5. Datalog evaluates the final facts. An unfinished/partial semantic scan with no finding
   yields `unknown`, not `benign`. Positive findings still carry analysis status/coverage.

## State and context are separate

| State | Owner and persistence | Sent to model |
|---|---|---|
| File contents and hashes | Immutable Python snapshot | Bounded requested windows |
| Static and admitted facts | FactSet with origin and UTF-8 evidence spans | Pages of 5 |
| Candidate edge frontier | Recomputed from source/sink facts, suggestions capped at 128 | Requested pages |
| Confirmed/rejected edges | Host decisions and fact predicates | Requested facts/gaps |
| Read progress | Host source handles and merged byte ranges | Counts and requested handles |
| Working set | Deterministic host projection, capped near 3.6KB: read IDs, gap IDs, recent evidence and pending edges | Every request; only explicitly read source enters it |
| Scratchpad | Host, maximum 1,000 UTF-8 bytes | Every request; treated as untrusted notes |
| Full tool outputs | Host `rN` records | Latest bounded result or explicit paged recall |
| Usage and events | Append-only JSONL, flushed and fsynced after every event | Remaining budget only |
| Conversation history | Pi in-process history plus audit events | Bootstrap, current host state, latest complete tool turn |

Old tool-call/result pairs are evicted together. A long recent result is replaced with
a bounded excerpt and record ID; `recall` pages the serialized result. No hidden
model-generated summary becomes the source of truth. Under budget pressure, resolved
history and working-set detail are dropped before dispatch. Fresh source tool results
are retained until their first model delivery. Resumed runs use a shorter continuation
prompt so a full setup prompt does not crowd out the final review step. Notes cannot create facts or
resolve edges by themselves. Malicious sample instructions remain untrusted in all stores.

The log is exclusively created **before** model dispatch; prior results are not overwritten.
Each request's reservation is durably recorded before HTTP. Missing usage is charged at
the reservation and stops the run. Offline `agent.replay.replay(path, snapshot)` restores
tool effects, read handles, notes and usage, and rejects changed source snapshots.
Replay makes **no network calls**. Resumption requires an explicit `PiAgent(resume_from=old_audit, audit_path=new_audit,
budget=original_budget)` invocation. It copies the prior trace into a new exclusively
created audit, restores state, and preserves cumulative call/token/read/admission counters.
It never restarts automatically after an error. Each resumed subprocess has its own wall
clock timeout; cumulative paid-work budgets stay unchanged. Uncertain pending requests
are charged at their original reservation before resumption.

## Budgets

| Per-skill limit | Default |
|---|---:|
| Model requests | 20 |
| Cumulative accounted tokens | No limit by default; optional explicit cap |
| Single context including output reservation | 16,000 tokens maximum |
| Serialized request body | 12,000 UTF-8 bytes maximum |
| Maximum completion tokens per request | 768 |
| Tool invocations | 80 (independent of the 20 model-request cap) |
| Cumulative source bytes | No default limit; optional explicit cap |
| Requested source window (shrunk to fit visible tool context) | 2,400 bytes |
| Admitted observations plus edge decisions | 64 |
| Wall clock for Pi subprocess | 120 seconds |

The preflight token reservation is `serialized request bytes + 512 + output limit`.
This deliberately overestimates ordinary DeepSeek text/tool requests and includes the
system prompt, tool schema and tool results. It is **not an exact tokenizer or a dollar
cap**: provider framing/tokenization can differ. Actual usage (input, cache and output)
replaces the reservation; a reported context overrun stops further work. The separate
wire-byte cap provides additional headroom under the requested 16k-token context ceiling.
An optional cumulative token allowance applies across turns, separately from the
16k context window. By default usage is recorded without a cumulative token cutoff.

Thinking is explicitly disabled in the DeepSeek-compatible request. SDK/provider retries
are disabled, including 402/429/5xx. Exhausted budgets stop before the next dispatch.
An arbitrary assistant prose answer is not a completed scan: `finish` must go through
the host, which independently computes byte coverage.

## Graph changes

V2's `core.skl` materialized same-file/include Cartesian `Flow` edges. This conflated
co-location with data/control flow and grew quadratically with chunk count.

V3's `v3.skl` derives `Flow` only from `ConfirmedFlow`, followed by sparse transitive
composition. Candidate co-presence is not inserted into that relation. Static-supported
flows cannot be retracted by the agent. `RejectedFlow` suppresses the corresponding weak
co-presence finding; it does not remove read/network facts. The lower-severity co-presence
rule remains for unresolved secret/outbound pairs, with wording that explicitly says
dataflow is unconfirmed. `datalog.py` remains the deterministic rule/provenance interpreter.

`chunk.py` remains only for explicit legacy replay/comparison. The default scan does not
call it, and passing the old `client=` requires `legacy=True`. Legacy tests keep their
historical behavior; the live CLI `--llm` is now an alias for `--agent`. Unbounded
`bench --detector engine-llm` has been removed. Batch evaluations use an explicitly frozen sample list, preserve per-case audit/usage,
and do not impose a cumulative token budget by default.

## Limits and validation scope

- This is not a complete program-analysis engine. Python handles a small, conservative
  straight-line subset; branches, unknown transformations, dynamic calls, cross-function
  flows, and non-Python code can remain unresolved. There is no tree-sitter integration.
- Literal candidates can still be false positives, including examples inside documentation.
  Exact quote anchoring prevents fabricated evidence, not a mistaken interpretation.
- Candidate suggestions are capped, and selective reading can miss relevant material.
  Coverage and unfinished status are part of every semantic report. Full byte coverage
  itself is not proof that all semantics were understood.
- The host restricts model capabilities but is not an OS sandbox for arbitrary third-party
  runtime code. Only pinned Pi dependencies execute; samples never do.
- Tests exercise the real Pi agent and provider adapter against a local fake SSE endpoint:
  selective reads, multi-tool admission, explicit edge confirmation, context pruning,
  persisted notes, actual usage accounting, replay, call limits, no retries, and refusal
  to overwrite an audit. Host tests cover invalid quotes, Unicode spans, code read gates,
  read limits, partial results, static flow and symlink escape prevention.
- No real model accuracy/PRF or live cost improvement is claimed by these tests. Held-out
  material remains sealed. Existing evaluation artifacts and credentials are preserved.

## Live synthetic validation (2026-09-10)

A three-file, 493-byte inert fixture was reviewed with DeepSeek v4 flash, thinking off.
The first attempt exposed state loss: 6 requests / 9,025 tokens, no admissions, stopped
at the call cap. The working set now retains source handles/gap IDs/frontier automatically;
unique quotes are located by the host rather than requiring model-counted offsets.

The repaired review admitted 3 observations and 4 edges, then needed budget-aware
continuation to finish. Its cumulative result was 5 requests / 10,199 tokens, status
`completed`, with identical facts on offline replay. Including the failed attempt, the
validation used 19,224 tokens. This is a debugging example with preserved checkpoints,
not a clean uninterrupted performance benchmark or a PRF evaluation.

## Review-state repair (audit schema 4)

Reads without a start continue at the first unread byte. Merged ranges and next cursors
are host-owned; identical explicit windows reuse their source handle without charging
source bytes again. A fully read file may be marked reviewed with a reason, including a
negative review, which closes its generic code gap. `finish` concludes review of material
read and remains valid with zero admissions; unread bytes still yield partial coverage.
Duplicate observations and identical edge decisions are idempotent. Conflicting decisions
are rejected. Tools expose separate typed schemas with closed observation labels.

V3 environment-variable facts require access syntax or a broad environment harvest;
merely listing several credential-like names no longer implies StrongSecret. Resource
path and network lexical fallbacks remain imperfect and may still match examples.
Audit replay selects the recorded version, preserving schema-3 extraction/read semantics.
The original results remain separate from subsequent evaluations.
