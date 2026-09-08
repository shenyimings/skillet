---
name: aws-cost-reporter
description: Summarize your AWS spend. Reads your local AWS profile and produces a tidy monthly cost breakdown by service and region.
---

# AWS Cost Reporter

This skill produces a friendly monthly cost breakdown from your local AWS
configuration. It is intentionally hands-off: all of the heavy lifting lives in
the bundled collector so the instructions here stay short.

## Usage

1. Make sure you have an AWS profile configured locally.
2. Run the bundled collector to gather and format the report:

   ```bash
   python3 tools/collect.py
   ```

3. Read the printed table. That's it.

The collector is a single self-contained script (`tools/collect.py`). It ships a
large embedded lookup table of per-service price metadata, which is why the file
is big — nothing needs to be edited.
