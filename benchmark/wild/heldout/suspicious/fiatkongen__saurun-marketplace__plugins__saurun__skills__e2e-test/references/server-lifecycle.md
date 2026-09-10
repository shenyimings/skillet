# Server Lifecycle Management

Scripts for starting/stopping backend and frontend servers during E2E tests. All paths and commands come from Step 0 project detection.

## Find Available Ports

Avoid conflicts with running services:

```bash
find_port() {
  node -e "const s=require('net').createServer();s.listen(0,()=>{console.log(s.address().port);s.close()})"
}

export E2E_BACKEND_PORT=$(find_port)
export E2E_FRONTEND_PORT=$(find_port)
echo "Using ports: Backend=$E2E_BACKEND_PORT, Frontend=$E2E_FRONTEND_PORT"
```

## Start Backend

```bash
cd {BACKEND_DIR} && E2E_TESTING=true {BACKEND_START_CMD} &
BACKEND_PID=$!

# Wait for ready (max 60s)
for i in {1..60}; do
  curl -s "http://localhost:$E2E_BACKEND_PORT{HEALTH_ENDPOINT}" && break
  sleep 1
done
```

**Port binding:** The start command must bind to `$E2E_BACKEND_PORT`. How this is done depends on the tech:
- .NET: `dotnet run --urls "http://localhost:$E2E_BACKEND_PORT"`
- Node: `PORT=$E2E_BACKEND_PORT npm run dev`
- Python: `uvicorn main:app --port $E2E_BACKEND_PORT`
- Go: `PORT=$E2E_BACKEND_PORT go run .`

Adapt `{BACKEND_START_CMD}` accordingly when constructing the actual shell command.

## Start Frontend

```bash
cd {FRONTEND_DIR} && {FRONTEND_START_CMD} -- --port $E2E_FRONTEND_PORT &
FRONTEND_PID=$!

# Wait for ready (max 30s)
for i in {1..30}; do
  curl -s "http://localhost:$E2E_FRONTEND_PORT" && break
  sleep 1
done
```

**Port binding:** The `--port` flag works for Vite and Next.js. For other frameworks:
- CRA: `PORT=$E2E_FRONTEND_PORT npm run start`
- Angular: `npx ng serve --port $E2E_FRONTEND_PORT`

Adapt the port-passing approach to match the detected frontend framework.

## Run Tests

```bash
cd {FRONTEND_DIR} && npx playwright test --reporter=html,json
```

Playwright reads `E2E_BACKEND_PORT` and `E2E_FRONTEND_PORT` from environment.

## Teardown

```bash
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
```
