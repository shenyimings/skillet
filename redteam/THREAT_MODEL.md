# Red-team threat model

## Attacker

Publishes a skill to an open registry. Has **white-box** knowledge of skillet: the rule
set (`rules/core.skl`), the extractors (`facts/`), the chunker and the labeller's schema.
Wants their skill to score `benign` while still achieving one of:

- **exfil** — read a secret (credential file, env var, key) and send it to an endpoint
  they control;
- **injection** — steer the agent against the user (authority claim + concealment, silent
  actions);
- **persistence** — write to agent memory/config so influence outlives the task.

## What counts

A skill in `redteam/` is malicious by construction, so the correct outcome is skillet
flagging it (`verdict != benign`), ideally with the right pattern. An attack **bypasses**
skillet when it scores `benign`.

A bypass is worth fixing when it has **defensive value**: the technique is realistic (a
real skill could plausibly look like this) and generalizable (fixing it closes a class,
not one string). A contrived one-off with no real-world analogue is recorded but not
chased — hardening against it would only add false-positive surface.

## Evaluation

`redteam/run.py` scans every attack and reports verdict + whether skillet caught it. Static
tier is the default (deterministic, free); attacks that specifically target the semantic
tier are marked and run with the LLM.
