# User Flow → Playwright Test Mapping

Guidelines for converting User Flows from product specs into Playwright tests.

## Input Format (From Spec)

User Flows in specs follow this pattern:

```markdown
## User Flows

### Create Recipe
1. User clicks "New Recipe" button in navbar
2. User fills in title, description, and cook time
3. User adds ingredients (name, quantity, unit)
4. User adds cooking steps
5. User clicks "Save"
6. System shows success toast and redirects to recipe detail page

### Browse Recipes
1. User navigates to home page
2. System displays recipe cards in a grid
3. User clicks a recipe card
4. System shows recipe detail page
```

## Output Format (Playwright Test)

Each User Flow becomes a test file in `{TEST_DIR}`.

### File Naming

```
User Flow Name → kebab-case.spec.ts

"Create Recipe" → create-recipe.spec.ts
"Browse Recipes" → browse-recipes.spec.ts
"Add Shopping Item" → add-shopping-item.spec.ts
```

### Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.beforeEach(async ({ request }) => {
  await request.post('/api/test/reset');
});

test('{Flow Name} flow', async ({ page }) => {
  // Step 1: {step description}
  await page.goto('/');
  await page.getByTestId('{component}-{element}').click();

  // Step 2: {step description}
  await page.getByTestId('{component}-{element}').fill('{value}');

  // Step N: {step description}
  await expect(page.getByTestId('{component}-{element}')).toBeVisible();
});
```

## Step → Action Mapping

| Step Pattern | Playwright Action |
|--------------|-------------------|
| User clicks "{button}" | `page.getByTestId('{id}').click()` |
| User fills in {field} | `page.getByTestId('{id}').fill('{value}')` |
| User selects {option} | `page.getByTestId('{id}').selectOption('{value}')` |
| User checks {checkbox} | `page.getByTestId('{id}').check()` |
| User navigates to {page} | `page.goto('{path}')` |
| System shows {element} | `await expect(page.getByTestId('{id}')).toBeVisible()` |
| System displays {text} | `await expect(page.getByText('{text}')).toBeVisible()` |
| System redirects to {page} | `await expect(page).toHaveURL('{pattern}')` |

## data-testid Inference

Derive `data-testid` from step context using the naming convention:

```
{component}-{element}-{action?}
```

Examples:
- "New Recipe button in navbar" → `navbar-new-recipe`
- "title field" in recipe form → `recipe-form-title`
- "Save button" in recipe form → `recipe-form-submit`
- "success toast" → `toast-success`
- "recipe card" → `recipe-card` or `recipe-card-{id}`

## Test Data

Use realistic test data:
- Strings: "Test Recipe", "A delicious test dish"
- Numbers: 30 (minutes), 4 (servings)
- IDs: Use fixed IDs for predictable assertions

## Complete Example

**User Flow:**
```markdown
### Create Recipe
1. User clicks "New Recipe" button in navbar
2. User fills in title, description, and cook time
3. User adds an ingredient (name: "Flour", quantity: "2", unit: "cups")
4. User clicks "Save"
5. System shows success toast
6. System redirects to recipe detail page
```

**Generated Test:**
```typescript
import { test, expect } from '@playwright/test';

test.beforeEach(async ({ request }) => {
  await request.post('/api/test/reset');
});

test('Create Recipe flow', async ({ page }) => {
  // Step 1: User clicks "New Recipe" button in navbar
  await page.goto('/');
  await page.getByTestId('navbar-new-recipe').click();

  // Step 2: User fills in title, description, and cook time
  await page.getByTestId('recipe-form-title').fill('Test Recipe');
  await page.getByTestId('recipe-form-description').fill('A delicious test dish');
  await page.getByTestId('recipe-form-cooktime').fill('30');

  // Step 3: User adds an ingredient
  await page.getByTestId('ingredient-form-name').fill('Flour');
  await page.getByTestId('ingredient-form-quantity').fill('2');
  await page.getByTestId('ingredient-form-unit').selectOption('cups');
  await page.getByTestId('ingredient-form-add').click();

  // Step 4: User clicks "Save"
  await page.getByTestId('recipe-form-submit').click();

  // Step 5: System shows success toast
  await expect(page.getByTestId('toast-success')).toBeVisible();

  // Step 6: System redirects to recipe detail page
  await expect(page).toHaveURL(/\/recipes\/\d+/);
});
```

## Multi-Flow Dependencies

If flows share setup (e.g., "Edit Recipe" requires a recipe to exist):

```typescript
test.describe('Recipe Management', () => {
  let recipeId: string;

  test.beforeEach(async ({ request }) => {
    // Reset DB then seed test data
    await request.post('/api/test/reset');
    const response = await request.post('/api/recipes', {
      data: { title: 'Test Recipe', cookTime: 30 }
    });
    recipeId = (await response.json()).id;
  });

  test('Edit Recipe flow', async ({ page }) => {
    await page.goto(`/recipes/${recipeId}/edit`);
    // ...
  });
});
```

## Assertions Best Practices

1. **Prefer `toBeVisible()` over `toBeInTheDocument()`** — tests actual visibility
2. **Use `toHaveURL()` with regex** — handles dynamic IDs
3. **Wait implicitly** — Playwright auto-waits, avoid explicit waits unless needed
4. **Test user-visible outcomes** — not implementation details
