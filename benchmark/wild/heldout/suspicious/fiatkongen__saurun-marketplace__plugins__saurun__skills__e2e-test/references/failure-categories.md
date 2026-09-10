# E2E Test Failure Categorization

Guidelines for diagnosing and categorizing E2E test failures.

## Categories

| Category | Description | Typical Resolution |
|----------|-------------|--------------------|
| `infra` | Environment/startup issues | Fix server startup, ports, dependencies |
| `app-code` | Application bug | Fix in frontend/backend source |
| `test-code` | Test selector/logic issue | Fix in test file |
| `flaky` | Intermittent, timing-related | Add waits, stabilize selectors |

---

## Detection Patterns

### `infra` — Infrastructure Issues

**Patterns:**
```
Error: connect ECONNREFUSED 127.0.0.1:{port}
Error: net::ERR_CONNECTION_REFUSED
Error: Timeout waiting for server to start
Error: Server process exited with code 1
```

**Diagnosis:**
- Backend didn't start → check backend start command output
- Frontend didn't start → check frontend start command output
- Port conflict → another process using the allocated port
- Missing dependencies → restore/install dependencies for the detected tech stack

**Resolution:**
- Kill conflicting processes
- Ensure correct working directory
- Check for missing environment variables

---

### `app-code` — Application Bugs

**Pattern 1: Element missing from DOM**
```
Error: locator.click: Error: strict mode violation: getByTestId('recipe-form-submit') resolved to 0 elements
```

AND the element should exist based on the User Flow spec.

**Diagnosis:** Component isn't rendering the element. Check:
- Component file for the `data-testid`
- Conditional rendering logic
- Route configuration

**Pattern 2: Assertion failed on content**
```
Error: expect(received).toBeVisible()
Received: element is not visible

Error: expect(received).toHaveText()
Expected: "Recipe saved"
Received: "Error: Failed to save"
```

**Diagnosis:** Application behavior doesn't match spec. Check:
- API response handling
- Error states
- Business logic

**Pattern 3: Navigation failure**
```
Error: expect(page).toHaveURL()
Expected pattern: /recipes/\d+/
Received: "http://localhost:{port}/recipes/new"
```

**Diagnosis:** Redirect not happening. Check:
- Form submission handler
- Router navigation calls
- API response handling

---

### `test-code` — Test Issues

**Pattern 1: Wrong selector**
```
Error: locator.click: Error: strict mode violation: getByTestId('recipe-submit') resolved to 0 elements
```

AND the element exists in DOM with a different `data-testid`.

**Diagnosis:** Test uses wrong selector. Check:
- Actual `data-testid` in component
- Naming convention adherence

**Pattern 2: Multiple matches**
```
Error: locator.click: Error: strict mode violation: getByTestId('item-delete') resolved to 3 elements
```

**Diagnosis:** Selector too generic. Fix:
- Use more specific selector: `getByTestId('item-delete-123')`
- Use `.first()`, `.nth(n)`, or filter

**Pattern 3: Wrong assertion**
```
Error: expect(received).toBeVisible()
// Element is present but hidden
```

**Diagnosis:** Test expects visibility but element is intentionally hidden. Check:
- Spec requirements
- Component conditional display logic

---

### `flaky` — Intermittent Failures

**Pattern 1: Timing-dependent**
```
Error: locator.click: Timeout 30000ms exceeded
// But works on retry
```

**Indicators:**
- Passes sometimes, fails sometimes
- Fails more in CI than locally
- Related to animations or async operations

**Diagnosis:** Race condition or animation. Fix:
- Add `waitFor` for dynamic content
- Use `toBeVisible({ timeout: 5000 })`
- Wait for network idle: `await page.waitForLoadState('networkidle')`

**Pattern 2: Order-dependent**
```
// Test A passes alone, fails after Test B
```

**Diagnosis:** Tests share state. Fix:
- Verify `beforeEach` calls `POST /api/test/reset`
- Verify backend started with `E2E_TESTING=true`
- Verify tests run serially (`workers: 1` in playwright config)

---

## Diagnosis Flow

```
Test Failed
│
├── Connection refused / timeout on startup?
│   └── YES → Category: infra
│
├── Element not found?
│   ├── Check DOM: element exists with different testid?
│   │   └── YES → Category: test-code (wrong selector)
│   └── Element truly missing?
│       └── YES → Category: app-code (component bug)
│
├── Assertion failed?
│   ├── Content mismatch (wrong text, wrong state)?
│   │   └── YES → Category: app-code
│   └── Visibility/timing issue?
│       └── YES → Category: flaky
│
├── Multiple elements matched?
│   └── YES → Category: test-code (generic selector)
│
└── Intermittent (passes sometimes)?
    └── YES → Category: flaky
```

---

## Fix Attempt Documentation

When logging fix attempts, include:

```markdown
### {Test Name} — Attempt {N}

**Error:**
```
{full error message}
```

**Category:** `{category}`

**Diagnosis:**
{what was identified as the root cause}

**Action:**
{what was changed}

**Files Modified:**
- `{file}:{line}` — {description of change}

**Result:** {Fixed | Still failing}
```

---

## Category Statistics

Track category distribution in the final report:

| Category | Count | % | Trend Notes |
|----------|-------|---|-------------|
| `infra` | 0 | 0% | Should be 0 after setup stabilizes |
| `app-code` | 3 | 60% | Primary source of real bugs |
| `test-code` | 1 | 20% | Reduce with better test generation |
| `flaky` | 1 | 20% | Target < 5% over time |

High `infra` count → Environment setup needs work
High `test-code` count → Test generation logic needs refinement
High `flaky` count → App needs stability improvements
