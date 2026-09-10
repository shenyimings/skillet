---
name: react-tdd
description: Use when implementing React + Vite + TypeScript features or bugfixes with Vitest + React Testing Library tests, before writing implementation code.
model: sonnet
disable-model-invocation: true
---

# React TDD — Enforcement Protocol

Mandatory TDD constraints for all React code. Violations must be fixed before committing.

## The Iron Laws

```
1. NO IMPLEMENTATION CODE WITHOUT A FAILING TEST FIRST
2. NEVER add test-only methods/props to production components
3. MOCK API BOUNDARIES ONLY (MSW) — never domain logic
4. COMMIT after each green cycle
```

Write code before test? Delete it. `git checkout .` — not stash, not "reference."

## Red-Green-Refactor

| Step | Action | Verify |
|------|--------|--------|
| RED | Write one failing test | Fails for expected reason (missing component, not typo) |
| GREEN | Write minimal code to pass | This test + all others pass |
| REFACTOR | Clean up, no new behavior | All tests still green |
| COMMIT | After each green cycle | `git commit` with passing tests |

## Mock Boundary Rule

**Mock API boundaries with MSW. NEVER mock domain logic or React internals.**

| OK to mock | NEVER mock |
|------------|------------|
| HTTP endpoints (MSW `http.get`, `http.post`) | Zustand stores |
| `window.location`, `navigator.*`, timers | React components |
| `IntersectionObserver`, `ResizeObserver` | Custom hooks |
| | Utility functions |

```tsx
// OK: MSW for API boundary
server.use(http.get('/api/products/:id', () => HttpResponse.json({ id: '1', name: 'Widget' })))

// VIOLATION
vi.mock('../stores/useCartStore')  // Never mock stores
vi.mock('./CartItem')              // Never mock components
```

`vi.mock` on a store, component, or hook is always a violation.

## What to Test

Test behavior, not structure. Ask: "If this test didn't exist, what bug could ship?"

**Priority:**
1. User-visible behavior (click, type, see result)
2. State transitions (store actions producing correct state)
3. Integration boundaries (component + API via MSW)
4. Edge cases (empty, null, boundary values)

**NEVER test:** className assertions, "renders without crashing", prop types, store getter values, hook return shapes.

## Test Structure Rules

- **Naming:** `it('should [behavior] when [condition]')` — "and" in name = split into two tests
- **Max 3 assertions** per test. Use `it.each` for parameterized cases.
- **Zero-assertion test** is always a violation. Every test needs `expect()`.
- **Shared render wrapper** — one custom render with providers, not inline wrapping per test.

## MSW Setup (copy into vitest.setup.ts)

```tsx
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Zustand in Tests

Use real stores. Reset in `beforeEach`. Never mock.

```tsx
beforeEach(() => {
  useCartStore.getState().reset()  // Use store's reset action
})
```

`vi.mock` on Zustand store is a violation. `useStore.setState()` to set values then asserting those same values is a violation — test through component interaction instead.

## Critical Anti-Patterns (auto-fail)

| Anti-Pattern | What it looks like | Fix |
|-------------|-------------------|-----|
| **StoreMock** | `vi.mock('../stores/useXStore')` | Use real store, reset in beforeEach |
| **ClassNameTest** | `expect(el).toHaveClass('bg-red-500')` | Test visible behavior, not CSS |
| **Assertionless** | `it('renders', () => { render(<X />) })` | Add expect() on visible content |
| **MockVerifyOnly** | Only assertion is `toHaveBeenCalled` | Assert on real UI outcome |
| **DirectSetState** | `setState(x)` then `expect(getState().x)` | Test through component interaction |
| **ProviderDuplicate** | Provider wrapping copy-pasted per test | Use shared custom render |

## Self-Review (before marking test done)

1. "Would this test catch a real bug?" — If no, delete it.
2. "Am I testing behavior or implementation details?" — If testing mock calls, stop.
3. "Did I watch this test fail first?" — If it passed immediately, it proves nothing.
4. "Is my test name a complete sentence?" — `should [x] when [y]`.

## Red Flags — Delete and Start Over

- Code before test / test passes immediately
- `vi.mock` on stores, components, or hooks
- className/style assertions
- Test with zero assertions
- More than 3 unrelated assertions without `it.each`
- "Already spent X hours, deleting is wasteful" — sunk cost. Delete.
