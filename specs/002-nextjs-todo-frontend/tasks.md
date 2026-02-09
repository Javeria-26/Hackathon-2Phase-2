# Tasks: Next.js Todo Frontend Application

**Input**: Design documents from `/specs/002-nextjs-todo-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-client.md

**Tests**: Tests are NOT included in this task list as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend project**: `frontend/` at repository root
- All paths relative to `frontend/` directory
- Next.js App Router: `app/` directory
- Components: `components/` directory
- Libraries: `lib/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Next.js 16+ project with TypeScript in frontend/ directory
- [ ] T002 Install core dependencies: next, react, react-dom, typescript, better-auth
- [ ] T003 [P] Configure TypeScript with tsconfig.json per plan.md specifications
- [ ] T004 [P] Configure ESLint and Prettier for code quality
- [ ] T005 [P] Create project directory structure: app/, components/, lib/, types/, styles/, public/
- [ ] T006 [P] Create environment variable template .env.example with NEXT_PUBLIC_API_URL and Better Auth config
- [ ] T007 [P] Configure next.config.js with required settings
- [ ] T008 [P] Create global styles in styles/globals.css with CSS reset and base styles
- [ ] T009 [P] Create root layout in app/layout.tsx with HTML structure and metadata

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Install and configure Better Auth library in lib/auth/better-auth.ts
- [ ] T011 Create Better Auth API routes in app/api/auth/[...auth]/route.ts
- [ ] T012 [P] Define TypeScript types for authentication in types/auth.ts (User, AuthState, Session)
- [ ] T013 [P] Define TypeScript types for todos in types/todo.ts (Todo, TodoListState, TodoFormData)
- [ ] T014 [P] Define TypeScript types for API in types/api.ts (ApiResponse, ApiError, ApiState)
- [ ] T015 Create AuthContext provider in lib/auth/auth-context.tsx with Better Auth integration
- [ ] T016 [P] Create custom auth hooks in lib/auth/auth-hooks.ts (useAuth, useSession)
- [ ] T017 Create base API client in lib/api/client.ts with JWT token injection and error handling
- [ ] T018 [P] Create todo API methods in lib/api/todos.ts (getAll, create, update, complete, delete)
- [ ] T019 [P] Create validation utilities in lib/utils/validation.ts (email, password, todo fields)
- [ ] T020 [P] Create storage utilities in lib/utils/storage.ts for browser storage helpers
- [ ] T021 [P] Create reusable UI components: Button in components/ui/Button.tsx
- [ ] T022 [P] Create reusable UI components: Input in components/ui/Input.tsx
- [ ] T023 [P] Create reusable UI components: LoadingSpinner in components/ui/LoadingSpinner.tsx
- [ ] T024 [P] Create reusable UI components: ErrorMessage in components/ui/ErrorMessage.tsx
- [ ] T025 Wrap root layout with AuthProvider in app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and First Login (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts and automatically log in to access the application

**Independent Test**: Navigate to registration page, submit valid credentials (email + password), verify account creation and automatic redirect to dashboard with empty todo list

### Implementation for User Story 1

- [ ] T026 [P] [US1] Create registration page in app/(auth)/register/page.tsx with route and basic structure
- [ ] T027 [P] [US1] Create RegisterForm component in components/auth/RegisterForm.tsx with email, password, confirmPassword fields
- [ ] T028 [US1] Implement form validation in RegisterForm (email format, password complexity, password match)
- [ ] T029 [US1] Implement registration submission logic in RegisterForm calling Better Auth register API
- [ ] T030 [US1] Add error handling and display in RegisterForm for validation and API errors
- [ ] T031 [US1] Add loading state during registration submission in RegisterForm
- [ ] T032 [US1] Implement auto-login after successful registration in RegisterForm
- [ ] T033 [US1] Add redirect to dashboard after successful registration in RegisterForm
- [ ] T034 [US1] Add link to login page from RegisterForm for existing users
- [ ] T035 [US1] Style RegisterForm with CSS Modules for responsive design

**Checkpoint**: User Story 1 complete - users can register and be automatically logged into dashboard

---

## Phase 4: User Story 2 - Returning User Login (Priority: P1) 🎯 MVP

**Goal**: Enable existing users to log in and access their personal dashboard

**Independent Test**: Navigate to login page, submit valid credentials for existing user, verify authentication and redirect to dashboard

### Implementation for User Story 2

- [ ] T036 [P] [US2] Create login page in app/(auth)/login/page.tsx with route and basic structure
- [ ] T037 [P] [US2] Create LoginForm component in components/auth/LoginForm.tsx with email and password fields
- [ ] T038 [US2] Implement form validation in LoginForm (email format, required fields)
- [ ] T039 [US2] Implement login submission logic in LoginForm calling Better Auth login API
- [ ] T040 [US2] Add error handling and display in LoginForm for invalid credentials
- [ ] T041 [US2] Add loading state during login submission in LoginForm
- [ ] T042 [US2] Implement redirect to dashboard after successful login in LoginForm
- [ ] T043 [US2] Add link to registration page from LoginForm for new users
- [ ] T044 [US2] Implement auto-redirect to dashboard if user already authenticated in login page
- [ ] T045 [US2] Style LoginForm with CSS Modules for responsive design
- [ ] T046 [P] [US2] Create homepage in app/page.tsx with links to login and register

**Checkpoint**: User Story 2 complete - existing users can log in and access dashboard

---

## Phase 5: User Story 3 - View Personal Todo List (Priority: P1) 🎯 MVP

**Goal**: Display authenticated user's todo list with all tasks showing title, description, and completion status

**Independent Test**: Log in as user with existing tasks, verify all tasks displayed correctly with visual distinction between completed and incomplete

### Implementation for User Story 3

- [ ] T047 [P] [US3] Create protected route layout in app/(protected)/layout.tsx with authentication check
- [ ] T048 [P] [US3] Implement authentication verification and redirect logic in protected layout
- [ ] T049 [P] [US3] Create dashboard page in app/(protected)/dashboard/page.tsx with basic structure
- [ ] T050 [P] [US3] Create TodoList component in components/todo/TodoList.tsx with loading and error states
- [ ] T051 [P] [US3] Create TodoItem component in components/todo/TodoItem.tsx to display single task
- [ ] T052 [US3] Implement todo fetching logic in dashboard page using todoApi.getAll
- [ ] T053 [US3] Extract user_id from auth context in dashboard page for API calls
- [ ] T054 [US3] Pass todos to TodoList component and render TodoItem for each task
- [ ] T055 [US3] Implement loading spinner display in TodoList while fetching
- [ ] T056 [US3] Implement error message display in TodoList if fetch fails
- [ ] T057 [US3] Create EmptyState component in components/todo/TodoList.tsx for no tasks scenario
- [ ] T058 [US3] Display empty state in TodoList when user has no tasks
- [ ] T059 [US3] Implement visual distinction for completed vs incomplete tasks in TodoItem (strikethrough, color)
- [ ] T060 [US3] Style TodoList and TodoItem with CSS Modules for responsive layout
- [ ] T061 [P] [US3] Create Header component in components/layout/Header.tsx with logo and user info
- [ ] T062 [P] [US3] Add Header to protected layout

**Checkpoint**: User Story 3 complete - users can view their complete todo list

---

## Phase 6: User Story 4 - Create New Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list with title and optional description

**Independent Test**: Click "Add Task" button, fill in title and description, submit, verify new task appears in list and persists in backend

### Implementation for User Story 4

- [ ] T063 [P] [US4] Create TodoForm component in components/todo/TodoForm.tsx with title and description fields
- [ ] T064 [US4] Implement form validation in TodoForm (title required 1-200 chars, description optional 0-1000 chars)
- [ ] T065 [US4] Implement form submission logic in TodoForm calling todoApi.create
- [ ] T066 [US4] Add error handling and display in TodoForm for validation and API errors
- [ ] T067 [US4] Add loading state during submission in TodoForm
- [ ] T068 [US4] Implement form reset after successful creation in TodoForm
- [ ] T069 [US4] Add "Add Task" button to dashboard page that opens TodoForm modal
- [ ] T070 [US4] Implement modal/dialog wrapper for TodoForm in dashboard page
- [ ] T071 [US4] Update todo list in dashboard page after successful task creation
- [ ] T072 [US4] Add cancel button to TodoForm that closes modal without saving
- [ ] T073 [US4] Style TodoForm with CSS Modules for responsive design

**Checkpoint**: User Story 4 complete - users can create new tasks (MVP COMPLETE!)

---

## Phase 7: User Story 5 - Update Existing Todo Task (Priority: P2)

**Goal**: Enable users to edit existing task details (title and description)

**Independent Test**: Click "Edit" on existing task, modify title/description, save, verify changes reflected in list and persisted

### Implementation for User Story 5

- [ ] T074 [P] [US5] Create TodoEditForm component in components/todo/TodoEditForm.tsx with pre-filled fields
- [ ] T075 [US5] Implement form validation in TodoEditForm (same rules as TodoForm)
- [ ] T076 [US5] Implement form submission logic in TodoEditForm calling todoApi.update
- [ ] T077 [US5] Add error handling and display in TodoEditForm for validation and API errors
- [ ] T078 [US5] Add loading state during submission in TodoEditForm
- [ ] T079 [US5] Add "Edit" button to TodoItem component
- [ ] T080 [US5] Implement modal/dialog wrapper for TodoEditForm in dashboard page
- [ ] T081 [US5] Pass selected todo to TodoEditForm for pre-filling
- [ ] T082 [US5] Update todo in list after successful edit in dashboard page
- [ ] T083 [US5] Add cancel button to TodoEditForm that closes modal without saving
- [ ] T084 [US5] Style TodoEditForm with CSS Modules for responsive design

**Checkpoint**: User Story 5 complete - users can edit existing tasks

---

## Phase 8: User Story 6 - Mark Todo Task as Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status with visual feedback

**Independent Test**: Click complete checkbox on task, verify visual update (strikethrough) and status persisted, click again to mark incomplete

### Implementation for User Story 6

- [ ] T085 [P] [US6] Add complete checkbox to TodoItem component
- [ ] T086 [US6] Implement checkbox toggle handler in TodoItem calling todoApi.complete
- [ ] T087 [US6] Implement optimistic update in dashboard page for complete action
- [ ] T088 [US6] Add rollback logic in dashboard page if complete API call fails
- [ ] T089 [US6] Update TodoItem visual styling based on completed state (strikethrough, color change)
- [ ] T090 [US6] Add loading indicator on checkbox during API call
- [ ] T091 [US6] Add error handling and display if complete action fails

**Checkpoint**: User Story 6 complete - users can mark tasks complete/incomplete

---

## Phase 9: User Story 7 - Delete Todo Task (Priority: P2)

**Goal**: Enable users to permanently delete tasks with confirmation to prevent accidents

**Independent Test**: Click "Delete" on task, confirm in dialog, verify task removed from list and backend

### Implementation for User Story 7

- [ ] T092 [P] [US7] Create DeleteConfirmDialog component in components/todo/DeleteConfirmDialog.tsx
- [ ] T093 [US7] Add "Delete" button to TodoItem component
- [ ] T094 [US7] Implement dialog open/close logic in dashboard page
- [ ] T095 [US7] Pass selected todo to DeleteConfirmDialog for display
- [ ] T096 [US7] Implement delete confirmation handler in DeleteConfirmDialog calling todoApi.delete
- [ ] T097 [US7] Implement optimistic update in dashboard page for delete action
- [ ] T098 [US7] Add rollback logic in dashboard page if delete API call fails
- [ ] T099 [US7] Add loading state during deletion in DeleteConfirmDialog
- [ ] T100 [US7] Add error handling and display if delete action fails
- [ ] T101 [US7] Style DeleteConfirmDialog with CSS Modules

**Checkpoint**: User Story 7 complete - users can delete tasks with confirmation

---

## Phase 10: User Story 8 - Session Persistence and Navigation (Priority: P2)

**Goal**: Maintain authentication state across page refreshes and navigation, implement logout

**Independent Test**: Log in, navigate between pages, refresh browser, verify auth state persists; click logout, verify session terminated

### Implementation for User Story 8

- [ ] T102 [P] [US8] Implement session persistence logic in AuthContext using Better Auth session
- [ ] T103 [US8] Add session restoration on app initialization in AuthContext
- [ ] T104 [US8] Implement token expiration detection in API client
- [ ] T105 [US8] Add automatic redirect to login on token expiration in API client
- [ ] T106 [US8] Implement logout function in AuthContext calling Better Auth logout
- [ ] T107 [US8] Add logout button to Header component
- [ ] T108 [US8] Implement logout handler in Header calling AuthContext.logout
- [ ] T109 [US8] Add redirect to login page after logout
- [ ] T110 [US8] Clear authentication state in AuthContext on logout
- [ ] T111 [US8] Add session expired message display when redirecting to login

**Checkpoint**: User Story 8 complete - session persists and logout works

---

## Phase 11: User Story 9 - Protected Route Access Control (Priority: P2)

**Goal**: Prevent unauthenticated access to protected routes with automatic redirect to login

**Independent Test**: Attempt to access /dashboard without authentication, verify redirect to login; access with auth, verify granted

### Implementation for User Story 9

- [ ] T112 [P] [US9] Create middleware.ts in frontend root for authentication checks
- [ ] T113 [US9] Implement authentication verification in middleware for protected routes
- [ ] T114 [US9] Add redirect to login for unauthenticated users in middleware
- [ ] T115 [US9] Enhance protected layout authentication check with loading state
- [ ] T116 [US9] Add redirect logic in protected layout for unauthenticated users
- [ ] T117 [US9] Implement expired session detection in protected layout
- [ ] T118 [US9] Add session expired message when redirecting from protected routes
- [ ] T119 [US9] Test protected route access without authentication
- [ ] T120 [US9] Test protected route access with valid authentication

**Checkpoint**: User Story 9 complete - protected routes secured

---

## Phase 12: User Story 10 - Responsive Mobile Experience (Priority: P3)

**Goal**: Ensure application works well on mobile devices with responsive layout and touch-friendly UI

**Independent Test**: Access application on mobile device (or emulator), verify layout adapts, all features work, touch targets appropriate

### Implementation for User Story 10

- [ ] T121 [P] [US10] Add responsive breakpoints to globals.css (mobile 320px, tablet 768px, desktop 1024px)
- [ ] T122 [P] [US10] Update Header component styles for mobile layout (hamburger menu or simplified nav)
- [ ] T123 [P] [US10] Update TodoList component styles for mobile layout (full width, optimized spacing)
- [ ] T124 [P] [US10] Update TodoItem component styles for mobile layout (larger touch targets, stacked layout)
- [ ] T125 [P] [US10] Update TodoForm component styles for mobile layout (full width inputs, stacked buttons)
- [ ] T126 [P] [US10] Update LoginForm component styles for mobile layout (full width, larger inputs)
- [ ] T127 [P] [US10] Update RegisterForm component styles for mobile layout (full width, larger inputs)
- [ ] T128 [US10] Test application on mobile device emulator (Chrome DevTools)
- [ ] T129 [US10] Test application on actual mobile device (iOS or Android)
- [ ] T130 [US10] Verify touch targets are minimum 44x44px on mobile
- [ ] T131 [US10] Test landscape and portrait orientations on mobile

**Checkpoint**: User Story 10 complete - application fully responsive

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T132 [P] Add loading states to all async operations across components
- [ ] T133 [P] Implement consistent error handling patterns across all components
- [ ] T134 [P] Add visual feedback for all user actions (button clicks, form submissions)
- [ ] T135 [P] Optimize bundle size by reviewing and removing unused dependencies
- [ ] T136 [P] Add proper TypeScript types to all components and functions
- [ ] T137 [P] Review and fix any ESLint warnings across codebase
- [ ] T138 [P] Add proper ARIA labels for accessibility
- [ ] T139 [P] Test keyboard navigation across all interactive elements
- [ ] T140 [P] Add proper meta tags for SEO in root layout
- [ ] T141 [P] Create README.md with setup and development instructions
- [ ] T142 [P] Update .env.example with all required environment variables
- [ ] T143 Run quickstart.md validation to ensure setup instructions work
- [ ] T144 Perform end-to-end testing of complete user journey (register → login → CRUD → logout)
- [ ] T145 Review all components for security vulnerabilities (XSS, injection)
- [ ] T146 Verify all API calls include JWT authentication tokens
- [ ] T147 Test error scenarios (network failures, API errors, invalid tokens)
- [ ] T148 Verify responsive design on multiple screen sizes (320px to 1920px)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-12)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 13)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories (can run parallel with US1)
- **User Story 3 (P1)**: Depends on US1 or US2 (need authentication) - Can run parallel with US4
- **User Story 4 (P1)**: Depends on US3 (need dashboard) - Sequential after US3
- **User Story 5 (P2)**: Depends on US3 and US4 (need todo list and CRUD foundation) - Can run parallel with US6, US7
- **User Story 6 (P2)**: Depends on US3 (need todo list) - Can run parallel with US5, US7
- **User Story 7 (P2)**: Depends on US3 (need todo list) - Can run parallel with US5, US6
- **User Story 8 (P2)**: Depends on US1 and US2 (need authentication) - Can run parallel with US5-7
- **User Story 9 (P2)**: Depends on US1, US2, US3 (need auth and protected routes) - Can run parallel with US5-8
- **User Story 10 (P3)**: Can start after any user story is complete - Affects all components

### Within Each User Story

- Tasks within a story should generally be executed in order
- Tasks marked [P] can run in parallel with other [P] tasks in the same story
- Complete all tasks in a story before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006, T007, T008, T009)
- All Foundational tasks marked [P] can run in parallel within Phase 2
- User Stories 1 and 2 can be developed in parallel (different components)
- User Stories 5, 6, 7 can be developed in parallel (different features on same foundation)
- User Story 8 and 9 can be developed in parallel with US5-7
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all type definitions together:
Task: "Define TypeScript types for authentication in types/auth.ts"
Task: "Define TypeScript types for todos in types/todo.ts"
Task: "Define TypeScript types for API in types/api.ts"

# Launch all UI components together:
Task: "Create reusable UI components: Button in components/ui/Button.tsx"
Task: "Create reusable UI components: Input in components/ui/Input.tsx"
Task: "Create reusable UI components: LoadingSpinner in components/ui/LoadingSpinner.tsx"
Task: "Create reusable UI components: ErrorMessage in components/ui/ErrorMessage.tsx"
```

## Parallel Example: User Story 1 & 2

```bash
# These can be developed simultaneously by different developers:
Developer A: User Story 1 (Registration)
- T026-T035: Registration page and form

Developer B: User Story 2 (Login)
- T036-T046: Login page and form
```

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T025) - CRITICAL
3. Complete Phase 3: User Story 1 - Registration (T026-T035)
4. Complete Phase 4: User Story 2 - Login (T036-T046)
5. Complete Phase 5: User Story 3 - View Todos (T047-T062)
6. Complete Phase 6: User Story 4 - Create Todos (T063-T073)
7. **STOP and VALIDATE**: Test complete user journey (register → login → view → create)
8. Deploy/demo MVP

**MVP Scope**: 73 tasks (T001-T073)
**MVP Delivers**: User registration, login, view todo list, create new todos

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T025)
2. Add User Stories 1-4 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 5 → Test independently → Deploy/Demo (Edit feature)
4. Add User Story 6 → Test independently → Deploy/Demo (Complete feature)
5. Add User Story 7 → Test independently → Deploy/Demo (Delete feature)
6. Add User Stories 8-9 → Test independently → Deploy/Demo (Session & Security)
7. Add User Story 10 → Test independently → Deploy/Demo (Mobile support)
8. Add Polish → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T025)
2. Once Foundational is done:
   - Developer A: User Story 1 (T026-T035)
   - Developer B: User Story 2 (T036-T046)
3. After US1 & US2:
   - Developer A: User Story 3 (T047-T062)
   - Developer B: User Story 4 (T063-T073)
4. After US3 & US4 (MVP complete):
   - Developer A: User Stories 5 & 6 (T074-T091)
   - Developer B: User Stories 7 & 8 (T092-T111)
   - Developer C: User Stories 9 & 10 (T112-T131)

---

## Task Summary

**Total Tasks**: 148 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 16 tasks
- Phase 3 (US1 - Registration): 10 tasks
- Phase 4 (US2 - Login): 11 tasks
- Phase 5 (US3 - View Todos): 16 tasks
- Phase 6 (US4 - Create Todos): 11 tasks
- Phase 7 (US5 - Update Todos): 11 tasks
- Phase 8 (US6 - Complete Todos): 7 tasks
- Phase 9 (US7 - Delete Todos): 10 tasks
- Phase 10 (US8 - Session Persistence): 10 tasks
- Phase 11 (US9 - Protected Routes): 9 tasks
- Phase 12 (US10 - Responsive Design): 11 tasks
- Phase 13 (Polish): 17 tasks

**MVP Scope**: 73 tasks (Phases 1-6)

**Parallel Opportunities**: 45+ tasks marked [P] can run in parallel

**Independent Test Criteria**: Each user story has clear independent test criteria defined

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP (User Stories 1-4) delivers core value: user onboarding and basic todo management
- Tests are NOT included as they were not explicitly requested in the specification
- All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
