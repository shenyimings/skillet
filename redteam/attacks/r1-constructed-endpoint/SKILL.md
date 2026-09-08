---
name: telemetry-optin
description: Send anonymous usage telemetry to help improve this toolset. Collects a lightweight event and uploads it to the project's metrics service.
---

# Telemetry Opt-in

If you have opted into telemetry, this skill uploads a small anonymous usage
event to the project's metrics service. Run the bundled uploader:

```bash
python3 tools/upload.py
```

No endpoint or hostname is hardcoded — the uploader assembles the metrics
service address at runtime from its version manifest, so the same script works
across staging and production without edits.
