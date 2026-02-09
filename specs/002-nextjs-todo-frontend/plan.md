# Implementation Plan: Next.js Todo Frontend Application

**Branch**: `002-nextjs-todo-frontend` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-nextjs-todo-frontend/spec.md`

## Summary

Build a responsive Next.js 16+ frontend application using App Router that enables authenticated users to manage their personal todo tasks. The application integrates Better Auth for user authentication, manages JWT tokens for secure API communication with a FastAPI backend, and provides a complete user interface for todo CRUD operations (create, read, update, delete, complete). The frontend enforces protected routes, handles authentication state persistence, and provides clear error handling and loading states across all operations.

**Technical Approach**: Implement a Next.js App Router application with Better Auth integration for authentication flows, React Context for authentication state management, a centralized API client for backend communication with JWT token injection, and responsive React components for the todo management interface.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 16+
**Primary Dependencies**: Next.js 16+, Better Auth, React 18+, TypeScript
**Storage**: Browser storage (localStorage/sessionStorage) for JWT token persistence
**Testing**: Jest with React Testing Library for component and integration testing
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile
**Project Type**: Web frontend (single-page application with App Router)
**Performance Goals**: Page load < 3 seconds, API requests < 5 seconds, UI interactions < 200ms feedback
**Constraints**: Responsive design 320px-1920px width, no backend logic, no database access, JWT-only authentication
**Scale/Scope**: Single-user frontend, support up to 1000 tasks per user, 10 routes, 20-30 components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development
- **Status**: PASS
- **Evidence**: Implementation follows approved specification from `specs/002-nextjs-todo-frontend/spec.md`
- **Compliance**: All requirements traced to spec, no implementation without specification

### ✅ II. Zero Manual Coding
- **Status**: PASS
- **Evidence**: Implementation will be performed via Claude Code using Agentic Dev Stack workflow
- **Compliance**: All code generation traceable to tasks, manual interventions documented in PHRs

### ✅ III. Security-First Design
- **Status**: PASS
- **Evidence**:
  - JWT tokens obtained from Better Auth and included in all API requests via Authorization header
  - Protected routes enforce authentication before access
  - User_id extracted from JWT claims, never from user input
  - No client-side trust of user identity
- **Compliance**: All security requirements from constitution enforced

### ✅ IV. Clear Separation of Concerns
- **Status**: PASS
- **Evidence**:
  - Frontend only - no backend logic or database access
  - Communicates with backend via documented REST API contracts
  - Depends on authentication feature (001-user-auth) for Better Auth configuration
  - No assumptions about backend internal implementation
- **Compliance**: Respects spec boundaries, uses only documented interfaces

### ✅ V. Production-Ready Architecture
- **Status**: PASS
- **Evidence**:
  - Comprehensive error handling for all API failures
  - Loading states for all asynchronous operations
  - Form validation before submission
  - Environment-based configuration via .env
  - Responsive design for all screen sizes
- **Compliance**: Meets all quality and operational requirements

### ✅ VI. Minimal Viable Changes
- **Status**: PASS
- **Evidence**: Implementation limited to specified features only, no speculative enhancements
- **Compliance**: No features outside spec, no unnecessary refactoring

### Technology Standards Compliance
- **Frontend Stack**: ✅ Next.js 16+ with App Router, Better Auth, Fetch API with JWT
- **API Contract**: ✅ Uses exact endpoint structure from constitution
- **Security**: ✅ JWT tokens via Authorization: Bearer header, protected routes
- **Development**: ✅ Claude Code workflow, Git feature branches, PHR documentation

**Overall Assessment**: All constitution gates PASS. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/002-nextjs-todo-frontend/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Better Auth integration patterns, JWT management
├── data-model.md        # Phase 1: Frontend data models and state structure
├── quickstart.md        # Phase 1: Development setup and running instructions
├── contracts/           # Phase 1: API contract definitions
│   └── api-client.md    # API endpoint contracts and request/response formats
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
frontend/                           # Next.js application root
├── app/                           # Next.js App Router directory
│   ├── layout.tsx                 # Root layout with auth provider
│   ├── page.tsx                   # Landing/home page
│   ├── (auth)/                    # Auth route group (public)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page
│   │   └── register/
│   │       └── page.tsx          # Registration page
│   ├── (protected)/               # Protected route group (requires auth)
│   │   ├── layout.tsx            # Protected layout with auth check
│   │   └── dashboard/
│   │       └── page.tsx          # Todo dashboard page
│   └── api/                       # API routes (if needed for Better Auth)
│       └── auth/
│           └── [...auth]/
│               └── route.ts      # Better Auth API routes
├── components/                    # React components
│   ├── auth/                     # Authentication components
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── todo/                     # Todo management components
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoForm.tsx
│   │   ├── TodoEditForm.tsx
│   │   └── DeleteConfirmDialog.tsx
│   ├── ui/                       # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorMessage.tsx
│   └── layout/                   # Layout components
│       ├── Header.tsx
│       └── Navigation.tsx
├── lib/                          # Utility libraries
│   ├── auth/                     # Authentication utilities
│   │   ├── better-auth.ts       # Better Auth configuration
│   │   ├── auth-context.tsx     # Auth context provider
│   │   └── auth-hooks.ts        # Custom auth hooks
│   ├── api/                      # API client
│   │   ├── client.ts            # Base API client with JWT injection
│   │   ├── todos.ts             # Todo API methods
│   │   └── types.ts             # API request/response types
│   └── utils/                    # General utilities
│       ├── validation.ts        # Form validation helpers
│       └── storage.ts           # Browser storage helpers
├── types/                        # TypeScript type definitions
│   ├── auth.ts                  # Authentication types
│   ├── todo.ts                  # Todo entity types
│   └── api.ts                   # API types
├── styles/                       # Global styles
│   └── globals.css              # Global CSS with responsive utilities
├── public/                       # Static assets
├── .env.local                    # Environment variables (not committed)
├── .env.example                  # Environment variable template
├── next.config.js                # Next.js configuration
├── tsconfig.json                 # TypeScript configuration
├── package.json                  # Dependencies and scripts
└── README.md                     # Project documentation

tests/                            # Test directory
├── components/                   # Component tests
│   ├── auth/
│   └── todo/
├── integration/                  # Integration tests
│   ├── auth-flow.test.tsx
│   └── todo-crud.test.tsx
└── setup.ts                      # Test setup and mocks
```

**Structure Decision**: Selected web application structure with Next.js App Router conventions. The `app/` directory uses route groups `(auth)` and `(protected)` to organize public and protected routes. Components are organized by feature (auth, todo, ui, layout) for maintainability. The `lib/` directory centralizes authentication logic, API client, and utilities. This structure follows Next.js 16+ best practices and supports the constitution's requirement for clear separation of concerns.

## Complexity Tracking

> **No violations - this section is empty**

All constitution requirements are met without exceptions. The implementation uses standard Next.js patterns and approved technologies.

---

## Phase 0: Research & Discovery

**Objective**: Resolve all technical unknowns and establish implementation patterns before design phase.

### Research Tasks

#### R1: Better Auth Integration with Next.js 16+ App Router

**Question**: How to properly integrate Better Auth with Next.js 16+ App Router for signup, signin, and JWT token management?

**Research Areas**:
- Better Auth installation and configuration for Next.js App Router
- Better Auth API route setup in `app/api/auth/[...auth]/route.ts`
- JWT token structure and claims provided by Better Auth
- Token storage best practices (localStorage vs sessionStorage vs cookies)
- Better Auth session management and token refresh patterns
- Better Auth TypeScript types and client-side hooks

**Success Criteria**:
- Clear understanding of Better Auth setup process
- Documented JWT token structure with user_id claim location
- Chosen token storage mechanism with security justification
- Example authentication flow from signup to authenticated request

**Output**: Document in `research.md` under "Better Auth Integration"

---

#### R2: Protected Route Implementation Patterns

**Question**: What is the best pattern for implementing protected routes in Next.js 16+ App Router?

**Research Areas**:
- Next.js App Router middleware for authentication checks
- Layout-based authentication enforcement
- Client-side vs server-side authentication checks
- Redirect patterns for unauthenticated users
- Loading states during authentication verification
- Handling authentication state on initial page load

**Success Criteria**:
- Chosen pattern for route protection with rationale
- Example implementation approach
- Handling of edge cases (expired tokens, invalid tokens, loading states)

**Output**: Document in `research.md` under "Protected Routes Pattern"

---

#### R3: API Client Architecture with JWT Injection

**Question**: How to structure the API client to automatically inject JWT tokens into all backend requests?

**Research Areas**:
- Fetch API wrapper patterns for token injection
- Request interceptor implementation
- Error handling for 401 Unauthorized responses
- Token expiration detection and handling
- Retry logic for failed requests
- TypeScript typing for API requests and responses

**Success Criteria**:
- API client architecture with automatic JWT injection
- Error handling strategy for authentication failures
- Type-safe API method signatures

**Output**: Document in `research.md` under "API Client Architecture"

---

#### R4: State Management Strategy

**Question**: What state management approach should be used for authentication state and todo data?

**Research Areas**:
- React Context vs external state library (Zustand, Redux)
- Authentication state management patterns
- Todo list state management (local state vs global state)
- Optimistic updates for todo operations
- State persistence across page refreshes
- State synchronization with backend

**Success Criteria**:
- Chosen state management approach with justification
- Authentication state structure
- Todo state structure and update patterns

**Output**: Document in `research.md` under "State Management Strategy"

---

#### R5: Form Validation and Error Handling

**Question**: What patterns should be used for form validation and error display?

**Research Areas**:
- Client-side validation libraries (React Hook Form, Formik, or native)
- Validation rules for email and password
- Real-time vs submit-time validation
- Error message display patterns
- Accessibility considerations for error messages
- Form state management (pristine, dirty, submitting)

**Success Criteria**:
- Chosen validation approach
- Validation rules for registration and login forms
- Error display patterns

**Output**: Document in `research.md` under "Form Validation Patterns"

---

#### R6: Responsive Design Implementation

**Question**: What approach should be used for responsive design across 320px-1920px screen widths?

**Research Areas**:
- CSS framework options (Tailwind CSS, CSS Modules, styled-components)
- Responsive breakpoints strategy
- Mobile-first vs desktop-first approach
- Touch-friendly UI patterns for mobile
- Responsive layout patterns for todo list
- Testing responsive designs

**Success Criteria**:
- Chosen CSS approach with rationale
- Defined breakpoints for mobile, tablet, desktop
- Responsive layout strategy

**Output**: Document in `research.md` under "Responsive Design Approach"

---

### Research Consolidation

**Deliverable**: `specs/002-nextjs-todo-frontend/research.md`

**Format**:
```markdown
# Research Findings: Next.js Todo Frontend

## Better Auth Integration
- **Decision**: [chosen approach]
- **Rationale**: [why chosen]
- **Alternatives Considered**: [other options evaluated]
- **Implementation Notes**: [key details]

## Protected Routes Pattern
[same structure]

## API Client Architecture
[same structure]

## State Management Strategy
[same structure]

## Form Validation Patterns
[same structure]

## Responsive Design Approach
[same structure]

## Summary
[key decisions and their implications]
```

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` completed with all decisions documented

### D1: Data Model Definition

**Objective**: Define frontend data models and state structures

**Deliverable**: `specs/002-nextjs-todo-frontend/data-model.md`

**Content**:

#### Authentication State Model
```typescript
interface AuthState {
  isAuthenticated: boolean
  isLoading: boolean
  user: User | null
  token: string | null
  error: string | null
}

interface User {
  id: string
  email: string
}
```

#### Todo Task Model
```typescript
interface Todo {
  id: string
  title: string
  description: string
  completed: boolean
  userId: string
  createdAt: string
  updatedAt: string
}
```

#### Form State Models
```typescript
interface LoginFormData {
  email: string
  password: string
}

interface RegisterFormData {
  email: string
  password: string
  confirmPassword: string
}

interface TodoFormData {
  title: string
  description: string
}
```

#### API State Models
```typescript
interface ApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

interface TodoListState extends ApiState<Todo[]> {}
```

**Validation Rules**:
- Email: Must match RFC 5322 format
- Password: Minimum 8 characters, at least one uppercase, one lowercase, one number, one special character
- Todo Title: Required, maximum 200 characters
- Todo Description: Optional, maximum 1000 characters

**State Transitions**:
- Authentication: unauthenticated → loading → authenticated | error
- Todo Operations: idle → loading → success | error
- Form Submission: pristine → dirty → submitting → submitted | error

---

### D2: API Contract Definition

**Objective**: Document all API endpoints and request/response formats

**Deliverable**: `specs/002-nextjs-todo-frontend/contracts/api-client.md`

**Content**:

#### Authentication Endpoints (Better Auth)
```
POST /api/auth/register
Request: { email: string, password: string }
Response: { user: User, token: string }
Status: 201 Created | 400 Bad Request | 409 Conflict

POST /api/auth/login
Request: { email: string, password: string }
Response: { user: User, token: string }
Status: 200 OK | 401 Unauthorized | 400 Bad Request

POST /api/auth/logout
Request: { }
Response: { success: boolean }
Status: 200 OK
```

#### Todo Endpoints (FastAPI Backend)
```
GET /api/{user_id}/tasks
Headers: Authorization: Bearer {jwt_token}
Response: { tasks: Todo[] }
Status: 200 OK | 401 Unauthorized | 403 Forbidden

POST /api/{user_id}/tasks
Headers: Authorization: Bearer {jwt_token}
Request: { title: string, description: string }
Response: { task: Todo }
Status: 201 Created | 400 Bad Request | 401 Unauthorized

GET /api/{user_id}/tasks/{id}
Headers: Authorization: Bearer {jwt_token}
Response: { task: Todo }
Status: 200 OK | 404 Not Found | 401 Unauthorized

PUT /api/{user_id}/tasks/{id}
Headers: Authorization: Bearer {jwt_token}
Request: { title: string, description: string }
Response: { task: Todo }
Status: 200 OK | 404 Not Found | 400 Bad Request | 401 Unauthorized

PATCH /api/{user_id}/tasks/{id}/complete
Headers: Authorization: Bearer {jwt_token}
Request: { completed: boolean }
Response: { task: Todo }
Status: 200 OK | 404 Not Found | 401 Unauthorized

DELETE /api/{user_id}/tasks/{id}
Headers: Authorization: Bearer {jwt_token}
Response: { }
Status: 204 No Content | 404 Not Found | 401 Unauthorized
```

#### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

---

### D3: Quickstart Guide

**Objective**: Provide setup and development instructions

**Deliverable**: `specs/002-nextjs-todo-frontend/quickstart.md`

**Content**:

#### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Backend API running (or mock API for development)

#### Environment Setup
```bash
# Clone repository
git clone <repo-url>
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Configure environment variables
# Edit .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

#### Development
```bash
# Run development server
npm run dev

# Open browser to http://localhost:3000

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Build for production
npm run build

# Start production server
npm start
```

#### Project Commands
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build production bundle
- `npm start` - Start production server
- `npm test` - Run test suite
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

#### Development Workflow
1. Start backend API (or use mock API)
2. Configure environment variables in `.env.local`
3. Run `npm run dev` to start development server
4. Access application at `http://localhost:3000`
5. Register a new user account
6. Test todo CRUD operations
7. Run tests with `npm test`

---

### D4: Component Architecture

**Objective**: Define component hierarchy and responsibilities

**Deliverable**: Document in `data-model.md` under "Component Architecture"

**Component Hierarchy**:

```
App (layout.tsx)
├── AuthProvider (auth-context.tsx)
├── Header (Header.tsx)
└── Page Content
    ├── (auth) - Public Routes
    │   ├── LoginPage
    │   │   └── LoginForm
    │   └── RegisterPage
    │       └── RegisterForm
    └── (protected) - Protected Routes
        └── DashboardPage
            ├── TodoList
            │   ├── TodoItem (multiple)
            │   │   ├── CompleteCheckbox
            │   │   ├── EditButton
            │   │   └── DeleteButton
            │   └── EmptyState
            ├── TodoForm (create)
            ├── TodoEditForm (edit modal)
            └── DeleteConfirmDialog
```

**Component Responsibilities**:

- **AuthProvider**: Manages authentication state, provides auth context
- **ProtectedRoute**: Enforces authentication, redirects unauthenticated users
- **LoginForm**: Handles login form submission, validation, error display
- **RegisterForm**: Handles registration form submission, validation, error display
- **TodoList**: Fetches and displays todos, handles loading and error states
- **TodoItem**: Displays single todo, handles complete/edit/delete actions
- **TodoForm**: Creates new todos, validates input, handles submission
- **TodoEditForm**: Edits existing todos, pre-fills form, handles updates
- **DeleteConfirmDialog**: Confirms deletion, prevents accidental deletes

---

## Phase 2: Task Generation

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, not `/sp.plan`.

The `/sp.tasks` command will:
1. Read this plan.md and research.md
2. Read data-model.md and contracts/
3. Generate tasks.md with ordered, testable implementation tasks
4. Include acceptance criteria for each task
5. Identify task dependencies

**Expected Task Categories**:
1. Project Setup & Configuration
2. Authentication Implementation
3. Protected Route Implementation
4. API Client Implementation
5. Todo CRUD Components
6. Form Validation & Error Handling
7. Responsive Design Implementation
8. Testing & Quality Assurance

---

## Architectural Decisions

### AD1: Better Auth for Authentication
**Decision**: Use Better Auth library for all authentication operations
**Rationale**:
- Constitution requirement for Better Auth
- Provides JWT token generation out of the box
- Integrates with Next.js App Router
- Handles session management
**Alternatives Considered**: Custom JWT implementation (rejected - violates constitution)
**Impact**: Simplifies authentication implementation, ensures JWT token compatibility with backend

### AD2: React Context for Authentication State
**Decision**: Use React Context API for authentication state management
**Rationale**:
- Authentication state is global and accessed by many components
- React Context is built-in, no external dependencies
- Sufficient for authentication state complexity
- Integrates well with Better Auth
**Alternatives Considered**: Zustand, Redux (rejected - unnecessary complexity for this scope)
**Impact**: Simple, maintainable authentication state management

### AD3: Centralized API Client with JWT Injection
**Decision**: Create a centralized API client that automatically injects JWT tokens
**Rationale**:
- Ensures all API requests include authentication
- Centralizes error handling for 401/403 responses
- Provides consistent API interface
- Simplifies component code
**Alternatives Considered**: Per-component API calls (rejected - duplicates token injection logic)
**Impact**: Consistent, secure API communication with minimal boilerplate

### AD4: Next.js App Router with Route Groups
**Decision**: Use App Router with (auth) and (protected) route groups
**Rationale**:
- App Router is Next.js 16+ standard
- Route groups organize public vs protected routes
- Enables layout-based authentication enforcement
- Supports nested layouts for shared UI
**Alternatives Considered**: Pages Router (rejected - outdated), flat route structure (rejected - less organized)
**Impact**: Clear route organization, easy authentication enforcement

### AD5: Component-Level State for Todo Operations
**Decision**: Use local component state for todo list and form state
**Rationale**:
- Todo data is page-specific, not global
- Simplifies state management
- Reduces complexity
- Sufficient for single-page todo list
**Alternatives Considered**: Global state (rejected - unnecessary for this scope)
**Impact**: Simple, maintainable component code

### AD6: Optimistic UI Updates
**Decision**: Implement optimistic updates for todo operations (complete, delete)
**Rationale**:
- Improves perceived performance
- Provides immediate user feedback
- Enhances user experience
- Can rollback on API failure
**Alternatives Considered**: Wait for API response (rejected - slower UX)
**Impact**: Better user experience, requires rollback logic for failures

---

## Security Considerations

### S1: JWT Token Storage
**Approach**: Store JWT tokens in httpOnly cookies (if Better Auth supports) or secure localStorage
**Rationale**:
- httpOnly cookies prevent XSS attacks
- localStorage is acceptable if XSS prevention is handled elsewhere
- Tokens must persist across page refreshes
**Mitigation**: Implement Content Security Policy, sanitize all user inputs

### S2: User ID Extraction
**Approach**: Always extract user_id from JWT token claims, never from user input
**Rationale**: Prevents users from accessing other users' data
**Implementation**: API client extracts user_id from token before making requests
**Validation**: Backend validates user_id matches authenticated user

### S3: Protected Route Enforcement
**Approach**: Check authentication on both client and server side
**Rationale**: Client-side for UX, server-side for security
**Implementation**: Middleware checks authentication, redirects unauthenticated users
**Fallback**: Backend enforces authentication even if frontend bypassed

### S4: Input Sanitization
**Approach**: Sanitize all user inputs before rendering
**Rationale**: Prevents XSS attacks
**Implementation**: Use React's built-in XSS protection, validate inputs
**Validation**: Reject inputs with suspicious patterns

### S5: HTTPS Enforcement
**Approach**: Use HTTPS in production for all API communication
**Rationale**: Prevents token interception
**Implementation**: Configure Next.js to redirect HTTP to HTTPS
**Validation**: Environment variable controls API URL scheme

---

## Performance Optimization

### P1: Code Splitting
**Approach**: Use Next.js automatic code splitting
**Benefit**: Faster initial page load
**Implementation**: Dynamic imports for large components

### P2: Image Optimization
**Approach**: Use Next.js Image component
**Benefit**: Optimized image loading
**Implementation**: Replace <img> with <Image>

### P3: API Response Caching
**Approach**: Cache todo list responses
**Benefit**: Reduces API calls
**Implementation**: Cache with revalidation on mutations

### P4: Lazy Loading
**Approach**: Lazy load non-critical components
**Benefit**: Faster initial render
**Implementation**: React.lazy for modals and dialogs

---

## Testing Strategy

### Unit Tests
- Component rendering tests
- Form validation logic tests
- API client method tests
- Utility function tests

### Integration Tests
- Authentication flow (register → login → dashboard)
- Todo CRUD flow (create → view → update → delete)
- Protected route access tests
- Error handling tests

### E2E Tests (Future)
- Full user journey tests
- Cross-browser compatibility tests
- Responsive design tests

---

## Deployment Considerations

### Environment Variables
```
NEXT_PUBLIC_API_URL=<backend-api-url>
NEXT_PUBLIC_BETTER_AUTH_URL=<auth-api-url>
BETTER_AUTH_SECRET=<secret-key>
```

### Build Process
1. Run type checking: `npm run type-check`
2. Run linting: `npm run lint`
3. Run tests: `npm test`
4. Build production bundle: `npm run build`
5. Deploy to hosting platform (Vercel, Netlify, etc.)

### Production Checklist
- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] Content Security Policy configured
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Analytics configured (optional)
- [ ] Performance monitoring configured

---

## Dependencies

### Required Dependencies
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "better-auth": "^latest",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/node": "^20.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^16.0.0"
  }
}
```

### Optional Dependencies (Based on Research)
- CSS Framework: Tailwind CSS (if chosen in research)
- Form Library: React Hook Form (if chosen in research)
- Validation Library: Zod (if chosen in research)

---

## Success Metrics

### Functional Metrics
- [ ] All 10 user stories implemented and tested
- [ ] All 30 functional requirements met
- [ ] All 15 success criteria achieved

### Quality Metrics
- [ ] Test coverage > 80%
- [ ] Zero TypeScript errors
- [ ] Zero ESLint errors
- [ ] Lighthouse score > 90

### Performance Metrics
- [ ] Page load < 3 seconds
- [ ] API requests < 5 seconds
- [ ] UI interactions < 200ms feedback
- [ ] Responsive 320px-1920px

---

## Next Steps

1. **Review this plan** with stakeholders for approval
2. **Execute Phase 0**: Complete research tasks, generate `research.md`
3. **Execute Phase 1**: Complete design tasks, generate `data-model.md`, `contracts/`, `quickstart.md`
4. **Run `/sp.tasks`**: Generate implementation tasks from this plan
5. **Run `/sp.implement`**: Execute implementation tasks
6. **Create ADRs**: Document significant architectural decisions
7. **Create PHR**: Document planning work

---

**Plan Status**: Ready for Phase 0 Research
**Next Command**: Begin research phase or proceed to `/sp.tasks` if research is complete
