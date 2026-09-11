// =============================================================================
// FILE: src/test/test-utils.tsx
// =============================================================================
import { render, type RenderOptions } from '@testing-library/react'
import { type ReactElement } from 'react'
import { MemoryRouter } from 'react-router-dom'

function AllProviders({ children }: { children: React.ReactNode }) {
  return (
    <MemoryRouter>
      {children}
    </MemoryRouter>
  )
}

function customRender(ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, { wrapper: AllProviders, ...options })
}

export * from '@testing-library/react'
export { customRender as render }

// =============================================================================
// FILE: src/test/setup.ts (or vitest.setup.ts)
// =============================================================================
// import { beforeEach } from 'vitest'
// import { useCartStore } from '../stores/useCartStore'
//
// beforeEach(() => {
//   useCartStore.getState().clearCart() // Use real store action, not setState
// })
