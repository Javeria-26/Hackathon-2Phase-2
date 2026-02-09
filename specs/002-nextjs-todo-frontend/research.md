# Research Findings: Next.js Todo Frontend

**Date**: 2026-02-08
**Feature**: 002-nextjs-todo-frontend
**Purpose**: Resolve technical unknowns before implementation

---

## Better Auth Integration

### Decision
Use Better Auth with Next.js 16+ App Router by installing the `better-auth` package and configuring it with API routes in `app/api/auth/[...auth]/route.ts`. JWT tokens will be automatically generated upon successful authentication and stored in httpOnly cookies by Better Auth.

### Rationale
- Better Auth is designed for Next.js App Router and provides first-class support
- Handles JWT token generation, signing, and validation automatically
- Provides built-in session management with secure cookie storage
- Includes TypeScript types and React hooks for client-side usage
- Supports email/password authentication out of the box

### Alternatives Considered
- **NextAuth.js**: More mature but heavier, may be overkill for this use case
- **Custom JWT implementation**: Violates constitution requirement for Better Auth
- **Clerk/Auth0**: Third-party services, adds external dependency and cost

### Implementation Notes
- Install: `npm install better-auth`
- Configure in `lib/auth/better-auth.ts` with JWT secret from environment
- JWT token structure includes: `{ userId, email, iat, exp }`
- Token expiration: 24 hours (per authentication spec)
- Better Auth provides `useSession()` hook for client-side auth state
- Better Auth provides `getSession()` for server-side auth checks

### JWT Token Structure
```typescript
interface JWTPayload {
  userId: string      // User ID for API requests
  email: string       // User email
  iat: number        // Issued at timestamp
  exp: number        // Expiration timestamp (24 hours)
}
```

### Token Storage
- **Method**: httpOnly cookies (Better Auth default)
- **Security**: Prevents XSS attacks, cookies not accessible via JavaScript
- **Persistence**: Cookies persist across browser sessions until expiration
- **CSRF Protection**: Better Auth includes CSRF token validation

---

## Protected Routes Pattern

### Decision
Use Next.js middleware combined with layout-based authentication checks. Middleware performs initial authentication verification and redirects unauthenticated users. Protected layouts verify authentication state and provide loading states.

### Rationale
- Middleware runs before page rendering, enabling server-side redirects
- Layout-based checks provide client-side authentication state
- Combines server-side security with client-side UX
- Supports loading states during authentication verification
- Prevents flash of unauthenticated content

### Alternatives Considered
- **Client-side only**: Insecure, can be bypassed
- **Server-side only**: Poor UX, no loading states
- **Higher-order components**: Outdated pattern for App Router

### Implementation Pattern

**Middleware** (`middleware.ts`):
```typescript
// Runs on every request to protected routes
// Checks for valid session cookie
// Redirects to /login if unauthenticated
// Allows request to proceed if authenticated
```

**Protected Layout** (`app/(protected)/layout.tsx`):
```typescript
// Wraps all protected pages
// Calls useSession() to get auth state
// Shows loading spinner while checking auth
// Redirects to /login if not authenticated
// Renders children if authenticated
```

### Edge Cases Handled
- **Expired tokens**: Middleware detects, redirects to login
- **Invalid tokens**: Middleware rejects, clears cookie, redirects
- **Loading states**: Layout shows spinner during auth check
- **Initial page load**: Middleware handles before React hydration

---

## API Client Architecture

### Decision
Create a centralized API client class that wraps the Fetch API and automatically injects JWT tokens from Better Auth session. The client provides typed methods for all backend endpoints and handles common error scenarios.

### Rationale
- Centralizes JWT token injection logic
- Provides consistent error handling
- Enables request/response interceptors
- Supports TypeScript for type safety
- Simplifies component code

### Alternatives Considered
- **Axios**: Additional dependency, Fetch API is sufficient
- **Per-component fetch calls**: Duplicates token injection logic
- **React Query**: Overkill for this scope, adds complexity

### Architecture

**Base Client** (`lib/api/client.ts`):
```typescript
class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async getAuthToken(): Promise<string | null> {
    // Get token from Better Auth session
    const session = await getSession()
    return session?.token || null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken()

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      // Token expired or invalid - redirect to login
      window.location.href = '/login'
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || 'Request failed')
    }

    if (response.status === 204) {
      return null as T
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Similar methods for PUT, PATCH, DELETE
}
```

**Todo API Methods** (`lib/api/todos.ts`):
```typescript
export const todoApi = {
  getAll: (userId: string) =>
    client.get<{ tasks: Todo[] }>(`/api/${userId}/tasks`),

  create: (userId: string, data: TodoFormData) =>
    client.post<{ task: Todo }>(`/api/${userId}/tasks`, data),

  update: (userId: string, id: string, data: TodoFormData) =>
    client.put<{ task: Todo }>(`/api/${userId}/tasks/${id}`, data),

  complete: (userId: string, id: string, completed: boolean) =>
    client.patch<{ task: Todo }>(`/api/${userId}/tasks/${id}/complete`, { completed }),

  delete: (userId: string, id: string) =>
    client.delete(`/api/${userId}/tasks/${id}`),
}
```

### Error Handling Strategy
- **401 Unauthorized**: Redirect to login, clear session
- **403 Forbidden**: Show error message, user lacks permission
- **404 Not Found**: Show "not found" message
- **400 Bad Request**: Show validation errors from response
- **500 Server Error**: Show generic error message
- **Network Error**: Show "connection failed" message with retry option

### User ID Extraction
- Extract `userId` from Better Auth session on client side
- Pass `userId` to all API methods
- Backend validates `userId` matches JWT token claims
- Never allow user to manually specify `userId`

---

## State Management Strategy

### Decision
Use React Context for authentication state and local component state for todo data. No external state management library needed.

### Rationale
- Authentication state is global and accessed by many components
- Todo data is page-specific and doesn't need global state
- React Context is built-in, no additional dependencies
- Sufficient complexity for this application scope
- Keeps implementation simple and maintainable

### Alternatives Considered
- **Zustand**: Lightweight but unnecessary for this scope
- **Redux**: Too heavy, adds significant complexity
- **Jotai/Recoil**: Atomic state management, overkill for this use case
- **React Query**: Good for server state but adds learning curve

### Authentication State Structure

**Context** (`lib/auth/auth-context.tsx`):
```typescript
interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

// Provider wraps entire app in root layout
// Uses Better Auth session under the hood
// Provides auth state and methods to all components
```

### Todo State Structure

**Component State** (in DashboardPage):
```typescript
const [todos, setTodos] = useState<Todo[]>([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)

// Fetch todos on mount
// Update local state on CRUD operations
// Optimistic updates for better UX
```

### Optimistic Updates
- **Complete/Uncomplete**: Update UI immediately, rollback on error
- **Delete**: Remove from UI immediately, rollback on error
- **Create**: Add to UI with temporary ID, replace with real ID on success
- **Update**: Update UI immediately, rollback on error

---

## Form Validation Patterns

### Decision
Use native HTML5 validation combined with custom validation logic. No external form library needed for this scope.

### Rationale
- HTML5 validation provides basic validation out of the box
- Custom validation logic for complex rules (password strength)
- Keeps bundle size small
- Sufficient for registration, login, and todo forms
- Easy to implement and maintain

### Alternatives Considered
- **React Hook Form**: Excellent library but adds dependency
- **Formik**: Older, heavier alternative
- **Zod + React Hook Form**: Best practice but overkill for this scope

### Validation Rules

**Email Validation**:
- HTML5 `type="email"` for basic format
- Custom regex for RFC 5322 compliance: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Required field validation

**Password Validation** (Registration):
- Minimum 8 characters
- At least one uppercase letter: `/[A-Z]/`
- At least one lowercase letter: `/[a-z]/`
- At least one number: `/[0-9]/`
- At least one special character: `/[!@#$%^&*]/`
- Required field validation

**Password Confirmation**:
- Must match password field
- Real-time validation on input

**Todo Title Validation**:
- Required field
- Maximum 200 characters
- Trim whitespace

**Todo Description Validation**:
- Optional field
- Maximum 1000 characters
- Trim whitespace

### Validation Timing
- **On blur**: Validate field when user leaves it
- **On submit**: Validate all fields before submission
- **Real-time**: Show password strength indicator as user types
- **Async**: Check email uniqueness on registration (if backend supports)

### Error Display Pattern
```typescript
interface FieldError {
  field: string
  message: string
}

// Display errors inline below each field
// Use red text and border for invalid fields
// Clear errors when user starts typing
// Show all errors on submit attempt
```

---

## Responsive Design Approach

### Decision
Use CSS Modules with mobile-first responsive design. Implement custom breakpoints without a CSS framework to keep bundle size minimal.

### Rationale
- CSS Modules provide scoped styles without additional dependencies
- Mobile-first approach ensures mobile optimization
- Custom breakpoints give full control
- No framework overhead (Tailwind would add ~50KB)
- Sufficient for this application's UI complexity

### Alternatives Considered
- **Tailwind CSS**: Excellent but adds bundle size and learning curve
- **styled-components**: Runtime CSS-in-JS, performance overhead
- **Emotion**: Similar to styled-components
- **Plain CSS**: No scoping, harder to maintain

### Breakpoints Strategy
```css
/* Mobile first - base styles for 320px+ */
.container {
  padding: 1rem;
}

/* Tablet - 768px+ */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 768px;
    margin: 0 auto;
  }
}

/* Desktop - 1024px+ */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

/* Large desktop - 1440px+ */
@media (min-width: 1440px) {
  .container {
    max-width: 1200px;
  }
}
```

### Responsive Layout Patterns

**Todo List**:
- Mobile: Single column, full width
- Tablet: Single column, max-width container
- Desktop: Single column with wider max-width

**Forms**:
- Mobile: Full width inputs, stacked buttons
- Tablet: Constrained width, stacked buttons
- Desktop: Constrained width, inline buttons where appropriate

**Navigation**:
- Mobile: Hamburger menu or bottom nav
- Tablet: Horizontal nav bar
- Desktop: Horizontal nav bar with more spacing

### Touch-Friendly UI
- Minimum touch target size: 44x44px (iOS guideline)
- Adequate spacing between interactive elements
- Larger form inputs on mobile
- Swipe gestures for delete (optional enhancement)

### Testing Strategy
- Test on Chrome DevTools device emulator
- Test on actual mobile devices (iOS, Android)
- Test at breakpoint boundaries (767px, 1023px, etc.)
- Test landscape and portrait orientations

---

## Summary

### Key Decisions

1. **Better Auth Integration**: Use Better Auth with httpOnly cookies for secure JWT token management
2. **Protected Routes**: Combine middleware and layout-based authentication checks
3. **API Client**: Centralized client with automatic JWT injection and error handling
4. **State Management**: React Context for auth, local state for todos
5. **Form Validation**: Native HTML5 + custom validation logic
6. **Responsive Design**: CSS Modules with mobile-first approach

### Technology Stack Finalized
- Next.js 16+ with App Router
- Better Auth for authentication
- TypeScript for type safety
- CSS Modules for styling
- Jest + React Testing Library for testing
- No additional state management or form libraries

### Implementation Readiness
All technical unknowns have been resolved. The implementation can proceed with:
- Clear authentication patterns
- Defined API client architecture
- Established state management approach
- Validated form validation strategy
- Responsive design guidelines

### Risk Mitigation
- Better Auth integration risk mitigated by using official patterns
- API integration risk mitigated by centralized client with error handling
- State management complexity mitigated by keeping it simple
- Responsive design risk mitigated by mobile-first approach

**Status**: Research complete, ready for Phase 1 (Design)
