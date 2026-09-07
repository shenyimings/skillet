# skillet benchmark

A labelled corpus of agent skills for measuring the detector, with an emphasis on **real,
attributed content** over synthetic mock-ups.

## What "real" means here, per class

| Provenance | Meaning | In this corpus |
|---|---|---|
| `real_disclosed` | Payload published verbatim in a security write-up, reproduced with citation and neutralised | 3 malicious (Reversec Labs) |
| `reconstructed` | Rebuilt from a case study that describes the behaviour but withholds the payload | 1 malicious (USENIX Sec '26 Email Skill) |
| `third_party_fixture` | Vendored from another scanner's test suite under its licence | 15 (SkillSpector, Apache-2.0) |
| `real_public` | Unmodified skill fetched live from a public registry | see limitation below |

Every row's origin is recorded in `manifest.yaml` (`provenance`, `source_url`, `licence`,
`label_source`). `label_source` in particular records *how* the label was assigned, so a
result is never stronger than its ground truth.

## Ground-truth dataset

Label distribution and the taxonomy weighting come from **MaliciousAgentSkillsBench v0.2**
(Liu et al., *"Do Not Mention This to the User"*, MIT licence,
<https://zenodo.org/records/20286334>): 98,380 real skills labelled `safe` / `suspicious`
/ `malicious`, of which 157 are behaviourally-confirmed malicious. The confirmed-malicious
rows are label-only with anonymised repositories — the payloads are deliberately **not**
redistributed by the authors — which is why our malicious samples come from disclosed
PoCs and case studies rather than from that CSV.

## Fetching real public samples

`scripts/fetch_upstream.py` reproducibly (seeded) pulls real `safe`/`suspicious` skills
from the 361 non-redacted download URLs in the dataset snapshot and lays them out as
corpus directories for labelling.

> **Environment limitation.** In this managed session, outbound access to arbitrary
> GitHub repositories is restricted to the session's scoped repos, so the fetcher cannot
> retrieve third-party skills here (it fails closed with a clear message). Run it in an
> environment with open GitHub egress to populate the `real_public` rows; the seed makes
> the selection deterministic. The curated real content above does not depend on it.

## Safety / inertness

The corpus contains real malicious skill content. It is kept inert by construction:

- No live attacker endpoints. Every network destination is rewritten to a
  reserved-for-documentation range (`TEST-NET` `203.0.113.0/24` / `198.51.100.0/24`,
  `example.net`), noted per sample.
- The test suite **reads** samples; it never executes them.
- Payloads are truncated to instructions where a full bundle would exceed 256 KiB.

## Structure

```
benchmark/
  manifest.yaml              ground truth, one row per corpus/ directory
  schema/manifest.schema.json JSON Schema the manifest validates against
  schema/taxonomy.yaml        machine-readable taxonomy (families, patterns, cred patterns)
  corpus/<id>/                one sample: SKILL.md plus any referenced files
  corpus/NOTICE               third-party attribution
```

## Using it

```python
from skillet.benchmark import load
from skillet.evaluator import evaluate
from skillet.baselines import keyword_baseline

report = evaluate(load(), keyword_baseline)
print(report.verdict.precision, report.verdict.recall)
```

`skillet bench --detector keyword` runs the same thing from the CLI.
