# Playwright Configuration Template

Use this configuration for E2E tests. Paths and ports are derived from Step 0 project detection.

## playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

// Dynamic ports from e2e-test skill, with fallback defaults for local dev
const BACKEND_PORT = process.env.E2E_BACKEND_PORT || '{DEFAULT_BACKEND_PORT}';
const FRONTEND_PORT = process.env.E2E_FRONTEND_PORT || '{DEFAULT_FRONTEND_PORT}';

export default defineConfig({
  testDir: '{TEST_DIR_RELATIVE}',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,  // Serial execution — DB isolation via /api/test/reset
  reporter: [
    ['html', { outputFolder: '{RESULTS_DIR}/playwright-report' }],
    ['json', { outputFile: '{RESULTS_DIR}/results.json' }],
  ],
  use: {
    baseURL: `http://localhost:${FRONTEND_PORT}`,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'on',  // Always record for demo artifacts
  },
  outputDir: '{RESULTS_DIR}/raw',
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  // webServer is optional when e2e-test skill manages server lifecycle
  // Uncomment for local development without the skill:
  // webServer: [
  //   {
  //     command: `cd {BACKEND_DIR} && {BACKEND_START_CMD}`,
  //     url: `http://localhost:${BACKEND_PORT}{HEALTH_ENDPOINT}`,
  //     reuseExistingServer: !process.env.CI,
  //     timeout: 60000,
  //   },
  //   {
  //     command: `{FRONTEND_START_CMD} -- --port ${FRONTEND_PORT}`,
  //     url: `http://localhost:${FRONTEND_PORT}`,
  //     reuseExistingServer: !process.env.CI,
  //     timeout: 30000,
  //   },
  // ],
});
```

**Note:** The `{RESULTS_DIR}` paths in reporter/outputDir should be relative to the playwright.config.ts location. Adjust the relative path prefix based on where the config lives (e.g., `../` if config is in `{FRONTEND_DIR}` and results dir is at project root).

## Port Configuration

The e2e-test skill finds available ports dynamically to avoid conflicts:

| Environment Variable | Purpose | Default |
|---------------------|---------|---------|
| `E2E_BACKEND_PORT` | Backend server port | `{DEFAULT_BACKEND_PORT}` |
| `E2E_FRONTEND_PORT` | Frontend dev server port | `{DEFAULT_FRONTEND_PORT}` |

**How it works:**
1. Skill finds 2 available ports before starting servers
2. Exports them as environment variables
3. Starts backend on `$E2E_BACKEND_PORT`
4. Starts frontend on `$E2E_FRONTEND_PORT`
5. Playwright reads ports from environment

**Local development:** If running Playwright manually without the skill, the framework-specific defaults are used.

## Key Settings Explained

| Setting | Value | Reason |
|---------|-------|--------|
| `video: 'on'` | Always record | Demo artifacts for stakeholders |
| `trace: 'retain-on-failure'` | Keep traces on fail | Debugging failed tests |
| `screenshot: 'only-on-failure'` | Capture on fail | Debugging context |
| `outputDir` | `{RESULTS_DIR}/raw` | Centralized artifact location |

## CI Environment

In CI (detected via `process.env.CI`):
- Retries set to 2 (handle flaky tests)
- `forbidOnly: true` (prevent `.only` from passing)

**Note:** `workers: 1` is set unconditionally (not just CI) to ensure DB isolation via `/api/test/reset` between tests.

## Custom Video Output

Videos are saved to `{RESULTS_DIR}/raw/` by Playwright. After test run, copy videos to `{RESULTS_DIR}/videos/` with friendly names:

```bash
# Post-test video organization
for f in {RESULTS_DIR}/raw/**/*.webm; do
  test_name=$(basename $(dirname $f))
  cp "$f" "{RESULTS_DIR}/videos/${test_name}.webm"
done
```
