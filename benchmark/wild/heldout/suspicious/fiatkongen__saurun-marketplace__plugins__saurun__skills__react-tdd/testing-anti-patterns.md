# React Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior or DOM structure. Mocks isolate API boundaries via MSW, not the thing being tested.

**Core principle:** Test what the user sees and does, not what the code internally calls.

**REFERENCE:** See SKILL.md for the Mock Boundary Rule and the full TDD cycle.

## Anti-Pattern Rules

```
1. NEVER test mock behavior — assert on real UI outcomes or store state
2. NEVER add test-only props or exports to production components
3. NEVER vi.mock Zustand stores, components, or custom hooks
4. ONE shared custom render wrapper, never duplicate provider setup
```

## Anti-Pattern 1: Mocking Zustand Stores

**Violation:**
```tsx
// BAD: Mocking the store prevents testing real behavior
vi.mock('../stores/useCartStore', () => ({
  useCartStore: () => ({
    items: [{ id: '1', name: 'Test', price: 10, quantity: 1 }],
    addItem: vi.fn(),
    removeItem: vi.fn(),
  })
}))

it('calls removeItem when remove clicked', async () => {
  render(<CartItem item={mockItem} />)
  await userEvent.click(screen.getByRole('button', { name: /remove/i }))
  expect(mockRemoveItem).toHaveBeenCalledWith('1') // Testing mock!
})
```

**Why wrong:** Tests the mock, not the cart behavior. Real store might have a bug in `removeItem` — this test would never catch it.

**Fix:** Use real store, assert real outcome.
```tsx
// GOOD: Real store, real behavior
beforeEach(() => {
  useCartStore.getState().clearCart()
  useCartStore.getState().addItem({ id: '1', name: 'Widget', price: 10, quantity: 1 })
})

it('should remove item from cart when remove button is clicked', async () => {
  render(<CartPage />)
  await userEvent.click(screen.getByRole('button', { name: /remove/i }))
  expect(screen.queryByText('Widget')).not.toBeInTheDocument()
})
```

### Gate Function

```
BEFORE using vi.mock on a store, component, or hook:
  Ask: "Am I mocking this because it's an API boundary?"
  IF no → STOP. Use the real thing.
  IF yes → Use MSW instead of vi.mock.
```

## Anti-Pattern 2: Testing CSS/ClassName

**Violation:**
```tsx
// BAD: Tests Tailwind class application, not behavior
it('applies destructive variant styles', () => {
  render(<Button variant="destructive">Delete</Button>)
  expect(screen.getByRole('button')).toHaveClass('bg-red-500')
})
```

**Why wrong:** Tests CSS framework integration, not your code's behavior. Tailwind already works. If you change the class name, this test fails even though behavior is identical.

**Fix:** Test what the user sees or can do.
```tsx
// GOOD: Test user-visible behavior
it('should show confirmation dialog when delete button is clicked', async () => {
  render(<DeleteButton onConfirm={vi.fn()} />)
  await userEvent.click(screen.getByRole('button', { name: /delete/i }))
  expect(screen.getByText(/are you sure/i)).toBeInTheDocument()
})
```

### Gate Function

```
BEFORE asserting on className, style, or CSS:
  Ask: "What bug would this catch?"
  IF "Tailwind class not applied" → STOP. That's Tailwind's job.
  IF "User can't see the error state" → Test for the visible text/role instead.
```

## Anti-Pattern 3: Renders Without Crashing

**Violation:**
```tsx
// BAD: Zero-assertion test — passes silently, catches nothing
it('renders without crashing', () => {
  render(<CartPage />)
})
```

**Why wrong:** Proves React.createElement works. Never catches a real bug. Inflates test count.

**Fix:** Always assert on something the user would see.
```tsx
// GOOD: Assert on visible content
it('should show cart heading when rendered', () => {
  render(<CartPage />)
  expect(screen.getByRole('heading', { name: /cart/i })).toBeInTheDocument()
})
```

### Gate Function

```
BEFORE writing any test:
  Ask: "Does this test have at least one expect() on visible behavior?"
  IF no → STOP. Add a real assertion or delete the test.
```

## Anti-Pattern 4: Test-Only Props

**Violation:**
```tsx
// BAD: testId prop only exists for tests
interface CartItemProps {
  item: CartItem
  testId?: string // Only used in tests!
}

export function CartItem({ item, testId }: CartItemProps) {
  return <div data-testid={testId}>...</div>
}
```

**Why wrong:** Pollutes production API. Use accessible roles/labels instead.

**Fix:** Query by role, text, or label.
```tsx
// GOOD: Query by accessible role
screen.getByRole('listitem', { name: item.name })
screen.getByLabelText(/quantity/i)
screen.getByText(item.name)
```

### Gate Function

```
BEFORE adding data-testid or test-only props:
  Ask: "Can I query this by role, text, or label?"
  IF yes → Use the accessible query. Remove the testId.
  IF no → The component has an accessibility problem. Fix that first.
```

## Anti-Pattern 5: Duplicate Provider Setup

**Violation:**
```tsx
// BAD: Copy-pasted provider wrapping in every test file
it('renders in router context', () => {
  render(
    <MemoryRouter>
      <QueryClientProvider client={new QueryClient()}>
        <CartPage />
      </QueryClientProvider>
    </MemoryRouter>
  )
})
```

**Why wrong:** Provider setup duplicated, inconsistent across files, hard to maintain.

**Fix:** Use shared custom render wrapper.
```tsx
// GOOD: Custom render from test-utils
import { render } from '../test/test-utils'

it('should show cart page with all providers', () => {
  render(<CartPage />)
  // Providers handled by wrapper
})
```

### Gate Function

```
BEFORE wrapping a component in providers in a test:
  Ask: "Does the custom render wrapper already handle this provider?"
  IF yes → Use custom render.
  IF no → Add the provider to the custom render wrapper, then use it everywhere.
```

## Anti-Pattern 6: Direct Store Testing

**Violation:**
```tsx
// BAD: Testing store in isolation when it should be tested through UI
it('adds item to store', () => {
  const { addItem } = useCartStore.getState()
  addItem({ id: '1', name: 'Widget', price: 10, quantity: 1 })
  expect(useCartStore.getState().items).toHaveLength(1)
})
```

**When wrong:** When the store action is only triggered by a component. Test through the component instead.

**When OK:** Pure computation logic (getTotal, discount calculations) that benefits from direct unit testing.

### Gate Function

```
BEFORE testing store directly:
  Ask: "Is this pure computation/logic, or is it triggered by UI?"
  IF pure computation → Direct store test is OK.
  IF triggered by UI → Test through component interaction.
```

## Quick Reference

| Anti-Pattern | Gate Question | Fix |
|--------------|---------------|-----|
| Mock Zustand stores | "Is this an API boundary?" | Use real store, assert real outcome |
| Test CSS/className | "What bug would this catch?" | Test visible behavior instead |
| Renders without crashing | "Does this have an assertion?" | Add real assertion or delete |
| Test-only props | "Can I query by role/text?" | Use accessible queries |
| Duplicate providers | "Does custom render handle this?" | Add to shared render wrapper |
| Direct store testing | "Pure logic or UI-triggered?" | Test through component if UI-triggered |

## Red Flags

These flags indicate test quality anti-pattern symptoms (what's wrong with the test). For TDD discipline violations (process problems), see SKILL.md Red Flags.

- `vi.mock` on stores, components, or hooks
- Assertions on `className`, `style`, or CSS variables
- Tests with zero `expect()` calls
- `data-testid` props in production components
- Provider setup copy-pasted across test files
- `vi.fn()` as only assertion target
- Store tested in isolation when behavior is UI-triggered
