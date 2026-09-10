# The evaluation set

Three pieces, with different jobs and very different label quality. Keeping them separate
matters more than the total count, because the headline metric each one supports is
different — and two of them cannot support the metric people usually quote.

| part | n | labels | what it can measure |
|---|---:|---|---|
| `benchmark/corpus/` (curated) | 19 | hand-reviewed, pattern-tagged | recall on known attack classes; per-pattern breakdown |
| `benchmark/wild/dev/` | 490 | dataset classification (`safe` 338 / `suspicious` 152) | false-positive rate on real skills |
| `benchmark/wild/heldout/` | 199 | dataset classification (`safe` 145 / `suspicious` 54) | **sealed** — generalisation, scored once |
| total | **708** | | |

## The held-out set

`scripts/fetch_wild.py` samples repositories from the MaliciousAgentSkillsBench ecosystem
snapshot, splits them 70/30 **by repository** (so dev and held-out never share an author's
house style), and materialises both halves — all before any content is inspected. Assignment
is seeded, and `benchmark/wild.lock.tsv` records the exact provenance of every sample (repo,
commit, path), so a fresh fetch reproduces the identical split.

The corpus content is checked in alongside the lockfile, so the evaluation set is stable
across machines and does not depend on 187 upstream repositories staying reachable. Binary
media (screenshots, demo GIFs, vendored databases) is stripped on the way in — see
`SKIP_PATTERNS` — since the scanner reads only text and the media was two thirds of the
bytes. Every sample keeps its upstream repo and commit in the lockfile for attribution.

The rule in `CLAUDE.md` is absolute: nothing in `benchmark/wild/heldout/` is read, listed,
grepped or scanned during development. `scripts/eval_wild.py heldout` prints aggregates only
— no sample ids, no paths, no spans — so that running it cannot become a way to read it.

### What the held-out set cannot tell you

**It contains no malicious samples, and no held-out set drawn from public data can.** The
dataset ships 157 behaviourally-confirmed malicious skills, but redacts their repositories:
0 of the 157 carry a live URL, against 116,060 of the safe rows and 361 of the suspicious
rows. Nobody publishes working payloads.

So the held-out set measures **false-positive rate on unseen real skills**, plus flag-rate on
unseen `suspicious`-labelled ones. It cannot measure malicious recall. Malicious recall is
measurable only on the curated 19 — every one of which the author has read while writing the
rules. That half of the evaluation is contaminated by construction, and no amount of
re-splitting fixes it; it needs new confirmed-malicious samples, which is a data-collection
problem, not a methodology one.

`suspicious` is also the dataset's own automated label, not a behavioural confirmation, so it
is reported as a flag rate rather than as recall.

## Why the old "precision = 1.00" was not worth reporting

The curated benchmark is 15 non-benign against 4 benign. The static tier flagged 5 samples,
all of them true positives, so precision came out 1.00. With four negatives in the set, that
number carries almost no information:

| statistic | point | 95% CI (Wilson) |
|---|---|---|
| precision, 5/5, curated benchmark | 1.00 | **[0.57, 1.00]** |
| FP rate, 0/4 benign, curated benchmark | 0% | **[0%, 49%]** |
| FP rate, 25/338 safe, `wild/dev` | 7.4% | [5.1%, 10.7%] |

A precision of 1.00 on this benchmark is consistent with a true false-positive rate anywhere
up to about a half. The benchmark simply does not contain enough negatives for a false
positive to have anywhere to show up — which is exactly why the FP rate had to be measured on
a separate corpus of real skills, and why that corpus is now part of the evaluation set
rather than a side experiment.

Report precision on the wild split, or not at all.

## Current numbers (static tier, rule set at `refactor/v2`)

    wild/dev safe        n=338   FP rate 25/338 = 7.4%
    wild/dev suspicious  n=152   flag rate 23/152 = 15.1%

Leading FP contributors on `safe`: `exfiltration_copresent` (16), `exfiltration` (14),
`exec_obfuscated` (7). The earlier 6% figure came from a 100-skill sample; 7.4% on 338 is the
better-powered estimate and is consistent with it.

## Reproducing

    python scripts/fetch_wild.py --safe 150 --suspicious 60   # clone + split (seeded)
    python scripts/eval_wild.py dev                           # development metric
    python scripts/eval_wild.py heldout                       # once, after rules are frozen
