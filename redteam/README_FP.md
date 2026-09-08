# False-positive measurement

`fp_test.py` scans a directory of **real benign skills** on the static tier and reports the
FP rate (any non-benign verdict = false positive) with a per-rule breakdown.

Because this environment blocks GitHub archive downloads but allows `git clone`, gather a
benign corpus by cloning real skill collections, e.g.:

    git clone --depth 1 https://github.com/anthropics/skills.git       benign_corpus/anthropics
    git clone --depth 1 https://github.com/obra/superpowers.git        benign_corpus/superpowers
    # plus a sample of 'safe'-labelled repos from MaliciousAgentSkillsBench (skills_dataset.csv)

    python redteam/fp_test.py benign_corpus/*

## Result (100 real benign skills, static tier)

| iteration | FP rate |
|---|---|
| v2 initial | 37% |
| + strong-secret gate, same-locus exec, drop co-presence/capability | 15% |
| + precise evasion gate (fold inside a security token) + socket-only reverse-shell + shell-rc-only persistence + large-run padding | **6%** |

The residual ~6% are edge cases (a couple of confusable/reverse-shell/over-privilege
findings on skills that genuinely do unusual things). Precision on the labelled benchmark
stays 1.00, and the red-team catches that depend on these rules were preserved (the
credential-file cross-file chain and the whitespace-truncation payload were recovered after
the first over-tightening).
