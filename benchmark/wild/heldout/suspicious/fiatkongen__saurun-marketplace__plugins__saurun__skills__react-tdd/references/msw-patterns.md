# MSW Patterns

## Global Setup

Add to `vitest.setup.ts`:

```tsx
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Per-Test Overrides

Override handlers for error cases in individual tests:

```tsx
import { server } from '../mocks/server'
import { http, HttpResponse } from 'msw'

it('should show error when API fails', async () => {
  server.use(
    http.get('/api/products/:id', () => HttpResponse.error())
  )
  // ...test
})
```

## Handler Organization

One `handlers.ts` per API domain, aggregated in `server.ts`.
