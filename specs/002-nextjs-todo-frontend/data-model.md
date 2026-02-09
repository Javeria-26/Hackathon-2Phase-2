# Data Model: Next.js Todo Frontend

**Date**: 2026-02-08
**Feature**: 002-nextjs-todo-frontend
**Purpose**: Define frontend data models, state structures, and component architecture

---

## Frontend Data Models

### Authentication Models

#### User
```typescript
interface User {
  id: string          // Unique user identifier from backend
  email: string       // User's email address
}
```

**Usage**: Stored in authentication context, displayed in UI header

---

#### AuthState
```typescript
interface AuthState {
  user: User | null           // Current authenticated user
  isAuthenticated: boolean    // Authentication status
  isLoading: boolean         // Loading state during auth operations
  error: string | null       // Error message from auth operations
}
```

**State Transitions**:
- Initial: `{ user: null, isAuthenticated: false, isLoading: true, error: null }`
- Loading: `{ user: null, isAuthenticated: false, isLoading: true, error: null }`
- Authenticated: `{ user: User, isAuthenticated: true, isLoading: false, error: null }`
- Error: `{ user: null, isAuthenticated: false, isLoading: false, error: string }`

---

#### Session
```typescript
interface Session {
  user: User          // User information
  token: string       // JWT token
  expiresAt: number   // Token expiration timestamp
}
```

**Storage**: Managed by Better Auth in httpOnly cookies
**Access**: Via `useSession()` hook or `getSession()` server function

---

### Todo Models

#### Todo
```typescript
interface Todo {
  id: string              // Unique task identifier
  title: string           // Task title (max 200 chars)
  description: string     // Task description (max 1000 chars)
  completed: boolean      // Completion status
  userId: string          // Owner user ID
  createdAt: string       // ISO 8601 timestamp
  updatedAt: string       // ISO 8601 timestamp
}
```

**Validation Rules**:
- `id`: Required, UUID format
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, 0-1000 characters, trimmed
- `completed`: Required, boolean
- `userId`: Required, matches authenticated user
- `createdAt`: Required, ISO 8601 format
- `updatedAt`: Required, ISO 8601 format

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the frontend implementation",
  "completed": false,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "createdAt": "2026-02-08T10:30:00Z",
  "updatedAt": "2026-02-08T10:30:00Z"
}
```

---

#### TodoListState
```typescript
interface TodoListState {
  todos: Todo[]           // Array of todos
  loading: boolean        // Loading state for fetch operations
  error: string | null    // Error message from API operations
}
```

**State Transitions**:
- Initial: `{ todos: [], loading: true, error: null }`
- Loading: `{ todos: [], loading: true, error: null }`
- Success: `{ todos: Todo[], loading: false, error: null }`
- Error: `{ todos: [], loading: false, error: string }`

---

### Form Models

#### LoginFormData
```typescript
interface LoginFormData {
  email: string       // User email
  password: string    // User password
}
```

**Validation**:
- `email`: Required, valid email format
- `password`: Required, minimum 1 character (no strength check on login)

---

#### RegisterFormData
```typescript
interface RegisterFormData {
  email: string              // User email
  password: string           // User password
  confirmPassword: string    // Password confirmation
}
```

**Validation**:
- `email`: Required, valid email format, unique (backend check)
- `password`: Required, minimum 8 characters, complexity requirements
- `confirmPassword`: Required, must match password

**Password Complexity Requirements**:
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&*)

---

#### TodoFormData
```typescript
interface TodoFormData {
  title: string           // Task title
  description: string     // Task description
}
```

**Validation**:
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, 0-1000 characters, trimmed

---

#### FormState
```typescript
interface FormState<T> {
  data: T                     // Form field values
  errors: Record<string, string>  // Field-level errors
  isSubmitting: boolean       // Submission in progress
  isDirty: boolean           // Form has been modified
}
```

**Usage**: Generic form state for all forms
**State Transitions**:
- Pristine: `{ data: T, errors: {}, isSubmitting: false, isDirty: false }`
- Dirty: `{ data: T, errors: {}, isSubmitting: false, isDirty: true }`
- Validating: `{ data: T, errors: {...}, isSubmitting: false, isDirty: true }`
- Submitting: `{ data: T, errors: {}, isSubmitting: true, isDirty: true }`
- Success: Form reset to pristine
- Error: `{ data: T, errors: {...}, isSubmitting: false, isDirty: true }`

---

### API Models

#### ApiResponse
```typescript
interface ApiResponse<T> {
  data: T                 // Response data
  status: number          // HTTP status code
  message?: string        // Optional message
}
```

---

#### ApiError
```typescript
interface ApiError {
  code: string            // Error code (e.g., "VALIDATION_ERROR")
  message: string         // Human-readable error message
  details?: Record<string, string>  // Field-level error details
}
```

**Example**:
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid input data",
  "details": {
    "email": "Email is already registered",
    "password": "Password must be at least 8 characters"
  }
}
```

---

#### ApiState
```typescript
interface ApiState<T> {
  data: T | null          // Response data
  loading: boolean        // Request in progress
  error: string | null    // Error message
}
```

**Usage**: Generic API state for async operations

---

## State Management Architecture

### Global State (React Context)

#### AuthContext
```typescript
interface AuthContextValue {
  // State
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean

  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}
```

**Provider Location**: Root layout (`app/layout.tsx`)
**Consumer Components**: All components needing auth state
**Implementation**: Uses Better Auth session under the hood

---

### Local State (Component State)

#### DashboardPage State
```typescript
const [todos, setTodos] = useState<Todo[]>([])
const [loading, setLoading] = useState<boolean>(true)
const [error, setError] = useState<string | null>(null)
const [editingTodo, setEditingTodo] = useState<Todo | null>(null)
const [deletingTodoId, setDeletingTodoId] = useState<string | null>(null)
```

**Scope**: Dashboard page only
**Updates**: On CRUD operations, optimistic updates

---

#### Form Component State
```typescript
const [formData, setFormData] = useState<FormData>(initialData)
const [errors, setErrors] = useState<Record<string, string>>({})
const [isSubmitting, setIsSubmitting] = useState<boolean>(false)
```

**Scope**: Individual form components
**Updates**: On input change, validation, submission

---

## Component Architecture

### Component Hierarchy

```
App (layout.tsx)
├── AuthProvider (auth-context.tsx)
│   └── Provides: user, isAuthenticated, login, register, logout
├── Header (Header.tsx)
│   ├── Logo
│   ├── Navigation
│   └── UserMenu (if authenticated)
│       └── Logout button
└── Page Content
    ├── (auth) - Public Routes
    │   ├── HomePage (page.tsx)
    │   │   ├── Hero section
    │   │   └── CTA buttons (Login, Register)
    │   ├── LoginPage (login/page.tsx)
    │   │   └── LoginForm
    │   │       ├── Email input
    │   │       ├── Password input
    │   │       ├── Submit button
    │   │       └── Link to Register
    │   └── RegisterPage (register/page.tsx)
    │       └── RegisterForm
    │           ├── Email input
    │           ├── Password input
    │           ├── Confirm password input
    │           ├── Submit button
    │           └── Link to Login
    └── (protected) - Protected Routes
        └── ProtectedLayout (layout.tsx)
            └── Checks authentication, redirects if needed
            └── DashboardPage (dashboard/page.tsx)
                ├── PageHeader
                │   ├── Title
                │   └── CreateTodoButton
                ├── TodoList
                │   ├── LoadingSpinner (if loading)
                │   ├── ErrorMessage (if error)
                │   ├── EmptyState (if no todos)
                │   └── TodoItem[] (if todos exist)
                │       ├── CompleteCheckbox
                │       ├── TodoContent
                │       │   ├── Title
                │       │   └── Description
                │       └── ActionButtons
                │           ├── EditButton
                │           └── DeleteButton
                ├── TodoFormModal (if creating)
                │   └── TodoForm
                │       ├── Title input
                │       ├── Description textarea
                │       ├── Cancel button
                │       └── Submit button
                ├── TodoEditModal (if editing)
                │   └── TodoEditForm
                │       ├── Title input (pre-filled)
                │       ├── Description textarea (pre-filled)
                │       ├── Cancel button
                │       └── Save button
                └── DeleteConfirmDialog (if deleting)
                    ├── Warning message
                    ├── Cancel button
                    └── Confirm button
```

---

### Component Responsibilities

#### AuthProvider
- **Purpose**: Manage global authentication state
- **State**: user, isAuthenticated, isLoading
- **Actions**: login, register, logout
- **Dependencies**: Better Auth
- **Consumers**: All components needing auth state

---

#### ProtectedRoute / ProtectedLayout
- **Purpose**: Enforce authentication on protected pages
- **Behavior**:
  - Check authentication state on mount
  - Show loading spinner while checking
  - Redirect to /login if not authenticated
  - Render children if authenticated
- **Dependencies**: AuthContext
- **Location**: `app/(protected)/layout.tsx`

---

#### LoginForm
- **Purpose**: Handle user login
- **State**: formData (email, password), errors, isSubmitting
- **Validation**: Email format, required fields
- **Actions**: Submit login, navigate to register
- **API**: POST /api/auth/login
- **Success**: Redirect to /dashboard
- **Error**: Display error message

---

#### RegisterForm
- **Purpose**: Handle user registration
- **State**: formData (email, password, confirmPassword), errors, isSubmitting
- **Validation**: Email format, password complexity, password match
- **Actions**: Submit registration, navigate to login
- **API**: POST /api/auth/register
- **Success**: Auto-login and redirect to /dashboard
- **Error**: Display error messages

---

#### TodoList
- **Purpose**: Display list of todos
- **State**: todos, loading, error
- **Behavior**:
  - Fetch todos on mount
  - Show loading spinner while fetching
  - Show error message if fetch fails
  - Show empty state if no todos
  - Render TodoItem for each todo
- **API**: GET /api/{user_id}/tasks
- **Dependencies**: AuthContext (for user_id)

---

#### TodoItem
- **Purpose**: Display single todo with actions
- **Props**: todo, onComplete, onEdit, onDelete
- **Behavior**:
  - Display title, description, completion status
  - Handle complete checkbox toggle
  - Handle edit button click
  - Handle delete button click
  - Visual distinction for completed tasks
- **Optimistic Updates**: Yes (for complete action)

---

#### TodoForm
- **Purpose**: Create new todo
- **State**: formData (title, description), errors, isSubmitting
- **Validation**: Title required (1-200 chars), description optional (0-1000 chars)
- **Actions**: Submit create, cancel
- **API**: POST /api/{user_id}/tasks
- **Success**: Close modal, refresh todo list
- **Error**: Display error message

---

#### TodoEditForm
- **Purpose**: Edit existing todo
- **Props**: todo (for pre-filling)
- **State**: formData (title, description), errors, isSubmitting
- **Validation**: Same as TodoForm
- **Actions**: Submit update, cancel
- **API**: PUT /api/{user_id}/tasks/{id}
- **Success**: Close modal, update todo in list
- **Error**: Display error message

---

#### DeleteConfirmDialog
- **Purpose**: Confirm todo deletion
- **Props**: todo (for display), onConfirm, onCancel
- **Behavior**:
  - Display warning message with todo title
  - Handle confirm button (calls onConfirm)
  - Handle cancel button (calls onCancel)
- **API**: DELETE /api/{user_id}/tasks/{id} (called by parent)
- **Optimistic Updates**: Yes (remove from list immediately)

---

## Data Flow Patterns

### Authentication Flow

1. **Registration**:
   - User submits RegisterForm
   - Form validates input
   - API call: POST /api/auth/register
   - Better Auth creates user, returns JWT token
   - Token stored in httpOnly cookie
   - AuthContext updates with user data
   - Redirect to /dashboard

2. **Login**:
   - User submits LoginForm
   - Form validates input
   - API call: POST /api/auth/login
   - Better Auth verifies credentials, returns JWT token
   - Token stored in httpOnly cookie
   - AuthContext updates with user data
   - Redirect to /dashboard

3. **Logout**:
   - User clicks logout button
   - API call: POST /api/auth/logout
   - Better Auth clears session cookie
   - AuthContext resets to unauthenticated state
   - Redirect to /login

---

### Todo CRUD Flow

1. **Fetch Todos**:
   - DashboardPage mounts
   - Get user_id from AuthContext
   - API call: GET /api/{user_id}/tasks
   - Update todos state with response
   - Render TodoList with todos

2. **Create Todo**:
   - User clicks "Add Task" button
   - TodoFormModal opens
   - User fills form and submits
   - API call: POST /api/{user_id}/tasks
   - Add new todo to todos state
   - Close modal

3. **Update Todo**:
   - User clicks "Edit" on TodoItem
   - TodoEditModal opens with pre-filled data
   - User modifies and submits
   - API call: PUT /api/{user_id}/tasks/{id}
   - Update todo in todos state
   - Close modal

4. **Complete Todo**:
   - User clicks complete checkbox
   - Optimistically update todo in state
   - API call: PATCH /api/{user_id}/tasks/{id}/complete
   - On success: Keep optimistic update
   - On error: Rollback optimistic update, show error

5. **Delete Todo**:
   - User clicks "Delete" on TodoItem
   - DeleteConfirmDialog opens
   - User confirms deletion
   - Optimistically remove todo from state
   - API call: DELETE /api/{user_id}/tasks/{id}
   - On success: Keep optimistic update
   - On error: Rollback optimistic update, show error

---

## Optimistic Update Patterns

### Complete/Uncomplete Todo
```typescript
// Optimistic update
const updatedTodos = todos.map(todo =>
  todo.id === id ? { ...todo, completed: !todo.completed } : todo
)
setTodos(updatedTodos)

// API call
try {
  await todoApi.complete(userId, id, !todo.completed)
  // Success - keep optimistic update
} catch (error) {
  // Rollback - revert to original state
  setTodos(todos)
  showError('Failed to update todo')
}
```

### Delete Todo
```typescript
// Optimistic update
const updatedTodos = todos.filter(todo => todo.id !== id)
setTodos(updatedTodos)

// API call
try {
  await todoApi.delete(userId, id)
  // Success - keep optimistic update
} catch (error) {
  // Rollback - restore deleted todo
  setTodos(todos)
  showError('Failed to delete todo')
}
```

---

## Validation Rules Summary

### Email Validation
- **Pattern**: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- **Required**: Yes
- **Max Length**: 255 characters
- **Trim**: Yes

### Password Validation (Registration)
- **Min Length**: 8 characters
- **Uppercase**: At least one (A-Z)
- **Lowercase**: At least one (a-z)
- **Number**: At least one (0-9)
- **Special**: At least one (!@#$%^&*)
- **Required**: Yes

### Todo Title Validation
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Required**: Yes
- **Trim**: Yes

### Todo Description Validation
- **Min Length**: 0 characters
- **Max Length**: 1000 characters
- **Required**: No
- **Trim**: Yes

---

## Error Handling Patterns

### Form Validation Errors
```typescript
interface ValidationErrors {
  [field: string]: string
}

// Example
{
  email: "Please enter a valid email address",
  password: "Password must be at least 8 characters",
  confirmPassword: "Passwords do not match"
}
```

### API Errors
```typescript
interface ApiError {
  code: string
  message: string
  details?: Record<string, string>
}

// Display strategy
- Show field-level errors inline below inputs
- Show general errors in alert/toast at top of form
- Clear errors when user starts typing
```

### Network Errors
```typescript
// Connection failed
"Unable to connect to server. Please check your internet connection."

// Timeout
"Request timed out. Please try again."

// Unknown error
"An unexpected error occurred. Please try again later."
```

---

## Performance Considerations

### Memoization
- Memoize expensive computations with `useMemo`
- Memoize callback functions with `useCallback`
- Prevent unnecessary re-renders with `React.memo`

### Lazy Loading
- Lazy load modals and dialogs with `React.lazy`
- Code split routes automatically with Next.js

### Debouncing
- Debounce search/filter inputs (if implemented)
- Debounce validation on input change

---

**Status**: Data model complete, ready for API contracts
