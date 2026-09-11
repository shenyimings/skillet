# Project Detection

Auto-detect project structure, tech stack, and paths. Run this as Step 0 before any other e2e-test steps.

## Detection Procedure

Execute these checks in order. Each section produces one or more config variables.

### 1. Project Layout

Determine if monorepo (separate frontend/backend dirs) or fullstack (single dir like Next.js).

```
Scan project root for directories:
  Frontend candidates: frontend/, client/, web/, app/, src/
  Backend candidates: backend/, server/, api/, Api/

If both a frontend and backend candidate exist → monorepo layout
If only one dir with both frontend deps + backend code → fullstack layout
If no clear separation → single-dir layout (FRONTEND_DIR = BACKEND_DIR = ".")
```

**Set:** `{FRONTEND_DIR}`, `{BACKEND_DIR}`

### 2. Frontend Tech & Start Command

```
Read {FRONTEND_DIR}/package.json:
  dependencies/devDependencies:
    "next"     → Next.js    → cmd: "npm run dev" (or "npx next dev")
    "vite"     → Vite       → cmd: "npm run dev" (or "npx vite")
    "react-scripts" → CRA  → cmd: "npm run start"
    "vue"      → Vue        → cmd: "npm run dev"
    "svelte"   → Svelte     → cmd: "npm run dev"
    "@angular/core" → Angular → cmd: "npm run start" (or "npx ng serve")

  Also check scripts section:
    Prefer "dev" script if it exists → "npm run dev"
    Fall back to "start" script → "npm run start"
    Fall back to "serve" script → "npm run serve"

Config files as confirmation:
  vite.config.ts/js     → Vite
  next.config.ts/js/mjs → Next.js
  angular.json          → Angular
  svelte.config.js      → Svelte
```

**Set:** `{FRONTEND_START_CMD}`, `{DEFAULT_FRONTEND_PORT}`

| Framework | Default Port |
|-----------|-------------|
| Vite | 5173 |
| Next.js | 3000 |
| CRA | 3000 |
| Vue CLI | 8080 |
| Angular | 4200 |
| SvelteKit | 5173 |

### 3. Backend Tech & Start Command

```
Scan {BACKEND_DIR} for:
  *.csproj           → .NET   → cmd: "dotnet run"
  package.json with express/fastify/koa/nestjs
                     → Node   → cmd: "npm run dev" or "npm start"
  requirements.txt / pyproject.toml / Pipfile
                     → Python → cmd: "uvicorn main:app" or "python -m flask run"
  go.mod             → Go     → cmd: "go run ."
  Cargo.toml         → Rust   → cmd: "cargo run"

For .NET, also check:
  If *.csproj is in a subdirectory (e.g., backend/Api/), set BACKEND_DIR to that subdirectory.
  Look for launchSettings.json → extract applicationUrl for default port.

For Node backends:
  Read package.json scripts → prefer "dev", then "start"
```

**Set:** `{BACKEND_START_CMD}`, `{DEFAULT_BACKEND_PORT}`

| Tech | Default Port |
|------|-------------|
| .NET | 5000 |
| Node (Express/Fastify) | 3000 |
| Python (FastAPI/Flask) | 8000 |
| Go | 8080 |
| Rust (Actix/Axum) | 8080 |

### 4. Backend Health Endpoint

```
Search {BACKEND_DIR} source for health endpoint registration:
  .NET: MapGet("/health"...), app.MapHealthChecks(...)
  Node: app.get("/health"...), router.get("/healthz"...)
  Python: @app.get("/health"), @app.route("/healthz")

If not found in source, try in order:
  /health → /healthz → /api/health → /ping → /

Set {HEALTH_ENDPOINT} to the first match found.
Fallback: "/"
```

**Set:** `{HEALTH_ENDPOINT}`

### 5. Test Directory

```
If {FRONTEND_DIR}/playwright.config.ts exists:
  Parse testDir value → use as TEST_DIR (resolved relative to config location)

Else if {FRONTEND_DIR}/e2e/ exists:
  TEST_DIR = "{FRONTEND_DIR}/e2e"

Else:
  TEST_DIR = "{FRONTEND_DIR}/e2e" (will be created)
```

**Set:** `{TEST_DIR}`, `{TEST_DIR_RELATIVE}` (relative to playwright.config.ts location)

### 6. Results Directory

```
If _docs/ exists in project root:
  RESULTS_DIR = "_docs/e2e-results"
Else:
  RESULTS_DIR = "e2e-results"
```

**Set:** `{RESULTS_DIR}`

### 7. Spec File Location

```
Search in order:
  _docs/specs/*-spec.md, _docs/specs/*.md (exclude *-architecture.md)
  docs/specs/*.md
  docs/*.spec.md
  specs/*.md
  *.spec.md (project root)

Use most recently modified match.
```

**Set:** `{SPEC_DIR}` (directory pattern for Step 1)

---

## Output Format

After detection, log the resolved config:

```
=== E2E Project Detection ===
Frontend dir:     {FRONTEND_DIR}
Backend dir:      {BACKEND_DIR}
Frontend cmd:     {FRONTEND_START_CMD}
Backend cmd:      {BACKEND_START_CMD}
Health endpoint:  {HEALTH_ENDPOINT}
Frontend port:    {DEFAULT_FRONTEND_PORT}
Backend port:     {DEFAULT_BACKEND_PORT}
Test dir:         {TEST_DIR}
Results dir:      {RESULTS_DIR}
Spec location:    {SPEC_DIR}
E2E env var:      E2E_TESTING=true
================================
```

If any critical item cannot be detected (BACKEND_DIR, FRONTEND_DIR, or their start commands), log a warning and ask the user for clarification. In autonomous mode (e.g., invoked by another skill), make the best guess from available evidence instead of blocking.

---

## Detection Priority Summary

| Item | Primary Strategy | Fallback |
|------|-----------------|----------|
| Frontend dir | Dir with package.json + frontend deps | `frontend/`, `client/`, `web/`, `src/`, `.` |
| Backend dir | Dir with `*.csproj`, server package.json, `requirements.txt` | `backend/`, `server/`, `api/`, `.` |
| Frontend cmd | package.json scripts → prefer `dev` | `npm run dev` |
| Backend cmd | Tech detection → framework convention | Ask user |
| Health endpoint | Source code search for route registration | `/health` → `/healthz` → `/` |
| Frontend port | Framework convention | Dynamic allocation |
| Backend port | Framework convention / launchSettings.json | Dynamic allocation |
| Test dir | Existing playwright.config.ts testDir | `{FRONTEND_DIR}/e2e/` |
| Results dir | `_docs/` exists → `_docs/e2e-results/` | `e2e-results/` |
| Spec files | `_docs/specs/`, `docs/specs/`, `docs/`, `specs/` | Require argument |
