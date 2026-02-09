# Tasks: FastAPI Todo Backend

**Input**: Design documents from `/specs/003-fastapi-todo-backend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this project uses:
- **Backend**: `backend/app/` for application code
- **Tests**: `backend/tests/` for test code
- **Root**: `backend/` for configuration files

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/app/, backend/tests/, backend/app/routers/)
- [x] T002 Create requirements.txt with dependencies: fastapi==0.109.0, uvicorn[standard]==0.27.0, sqlmodel==0.0.14, asyncpg==0.29.0, psycopg2-binary==2.9.9, python-jose[cryptography]==3.3.0, pydantic-settings==2.1.0, python-dotenv==1.0.0, pytest==7.4.4, pytest-asyncio==0.23.3, httpx==0.26.0
- [x] T003 [P] Create .env.example with JWT_SECRET_KEY, DATABASE_URL, FRONTEND_URL, ENVIRONMENT, DEBUG placeholders
- [x] T004 [P] Create pytest.ini with asyncio_mode=auto configuration
- [x] T005 [P] Create backend/app/__init__.py (empty)
- [x] T006 [P] Create backend/app/routers/__init__.py (empty)
- [x] T007 [P] Create backend/tests/__init__.py (empty)
- [x] T008 [P] Create .gitignore with .env, __pycache__/, *.pyc, venv/, .pytest_cache/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Database

- [x] T009 Implement config.py with Pydantic Settings class for JWT_SECRET_KEY, JWT_ALGORITHM, DATABASE_URL, FRONTEND_URL in backend/app/config.py
- [x] T010 Implement database.py with async engine, session factory, get_session dependency, create_db_and_tables function in backend/app/database.py
- [x] T011 Implement Todo SQLModel in backend/app/models.py with id (UUID), user_id (indexed), title (1-200 chars), description (0-1000 chars), completed (boolean), created_at, updated_at

### Authentication (User Story 2 - P1)

**Goal**: Implement JWT verification to secure all API endpoints

**Independent Test**: Can test by sending requests without token (401), with invalid token (401), with valid token (success)

- [x] T012 [US2] Implement JWT verification in backend/app/auth.py with verify_token function checking both 'sub' and 'userId' claims, get_current_user_id dependency
- [x] T013 [US2] Create test fixtures in backend/tests/conftest.py with test_user_id, auth_token (mock JWT), auth_headers, test database session, test client
- [x] T014 [P] [US2] Write test_missing_token in backend/tests/test_auth.py to verify 401 when Authorization header missing
- [x] T015 [P] [US2] Write test_invalid_token in backend/tests/test_auth.py to verify 401 with invalid token
- [x] T016 [P] [US2] Write test_expired_token in backend/tests/test_auth.py to verify 401 with expired token
- [x] T017 [P] [US2] Write test_valid_token in backend/tests/test_auth.py to verify 200 with valid token

### Application Setup

- [x] T018 Implement FastAPI app initialization in backend/app/main.py with lifespan context manager, CORS middleware configuration, global exception handlers for validation and JWT errors
- [x] T019 Add error response format with error.code, error.message, error.details structure to exception handlers in backend/app/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Personal Todos (Priority: P1) 🎯 MVP

**Goal**: Implement complete CRUD operations for todos with user isolation

**Independent Test**: Authenticate a user, create a todo, verify it appears in list, update it, delete it. Verify user cannot access other users' todos.

### CRUD Operations Implementation

- [x] T020 [P] [US1] Implement get_todos_by_user in backend/app/crud.py with user_id filtering, ordered by created_at DESC
- [x] T021 [P] [US1] Implement get_todo_by_id in backend/app/crud.py with user_id and todo_id filtering
- [x] T022 [P] [US1] Implement create_todo in backend/app/crud.py with user_id assignment, UUID generation
- [x] T023 [P] [US1] Implement update_todo in backend/app/crud.py with updated_at timestamp update
- [x] T024 [P] [US1] Implement delete_todo in backend/app/crud.py

### API Endpoints

- [x] T025 [US1] Implement POST /todos endpoint in backend/app/routers/todos.py with TodoCreate schema, 201 status, user_id from JWT
- [x] T026 [US1] Implement GET /todos endpoint in backend/app/routers/todos.py returning list of TodoResponse, user_id from JWT
- [x] T027 [US1] Implement GET /todos/{id} endpoint in backend/app/routers/todos.py with 404 if not found, user_id verification
- [x] T028 [US1] Implement PUT /todos/{id} endpoint in backend/app/routers/todos.py with TodoUpdate schema, 404 if not found, user_id verification
- [x] T029 [US1] Implement DELETE /todos/{id} endpoint in backend/app/routers/todos.py with 204 status, 404 if not found, user_id verification
- [x] T030 [US1] Register todos router in backend/app/main.py with /todos prefix

### Testing

- [x] T031 [P] [US1] Write test_create_todo in backend/tests/test_todos.py verifying 201 status, returned todo has id, user_id, timestamps
- [x] T032 [P] [US1] Write test_list_todos in backend/tests/test_todos.py verifying 200 status, returns array
- [x] T033 [P] [US1] Write test_get_todo in backend/tests/test_todos.py verifying 200 status, correct todo returned
- [x] T034 [P] [US1] Write test_get_todo_not_found in backend/tests/test_todos.py verifying 404 for non-existent ID
- [x] T035 [P] [US1] Write test_update_todo in backend/tests/test_todos.py verifying 200 status, updated fields, updated_at changed
- [x] T036 [P] [US1] Write test_delete_todo in backend/tests/test_todos.py verifying 204 status, todo removed from database
- [x] T037 [P] [US1] Write test_user_isolation in backend/tests/test_isolation.py verifying User A cannot access User B's todos (404 returned)
- [x] T038 [P] [US1] Write test_validation_empty_title in backend/tests/test_todos.py verifying 422 for empty title
- [x] T039 [P] [US1] Write test_validation_title_too_long in backend/tests/test_todos.py verifying 422 for title > 200 chars

**Checkpoint**: At this point, User Story 1 (CRUD operations) should be fully functional and testable independently. This is the MVP.

---

## Phase 4: User Story 3 - Filter and Query Todos (Priority: P2)

**Goal**: Add filtering by completion status and text search to enhance usability

**Independent Test**: Create todos with different statuses and titles, query with filters (?completed=true, ?search=meeting), verify only matching todos returned

### Filtering Implementation

- [x] T040 [US3] Add completed parameter to get_todos_by_user in backend/app/crud.py with optional boolean filter
- [x] T041 [US3] Add search parameter to get_todos_by_user in backend/app/crud.py with case-insensitive ILIKE on title and description
- [x] T042 [US3] Update GET /todos endpoint in backend/app/routers/todos.py to accept completed and search query parameters

### Testing

- [x] T043 [P] [US3] Write test_filter_by_completed in backend/tests/test_todos.py verifying ?completed=true returns only completed todos
- [x] T044 [P] [US3] Write test_filter_by_incomplete in backend/tests/test_todos.py verifying ?completed=false returns only incomplete todos
- [x] T045 [P] [US3] Write test_search_by_title in backend/tests/test_todos.py verifying ?search=meeting returns todos with "meeting" in title
- [x] T046 [P] [US3] Write test_search_by_description in backend/tests/test_todos.py verifying search works on description field
- [x] T047 [P] [US3] Write test_combined_filters in backend/tests/test_todos.py verifying ?completed=true&search=work returns todos matching both criteria

**Checkpoint**: At this point, User Stories 1 AND 3 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and final touches

- [x] T048 [P] Create README.md in backend/ with setup instructions, environment variables, running the server, API endpoints summary
- [x] T049 [P] Add input validation to TodoCreate and TodoUpdate schemas in backend/app/models.py with field validators for title (strip whitespace, non-empty)
- [x] T050 Run all tests with pytest to verify complete functionality
- [x] T051 Validate quickstart.md instructions by following setup steps
- [x] T052 [P] Add database connection error handling in backend/app/database.py to return 503 on connection failures
- [x] T053 [P] Add startup validation in backend/app/main.py to check JWT_SECRET_KEY is set

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion - MVP
- **User Story 3 (Phase 4)**: Depends on Foundational phase completion - Can run in parallel with US1 if desired, but builds on US1 endpoints
- **Polish (Phase 5)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Implemented in Foundational phase - Required for all endpoints
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable
- **User Story 4 (P2)**: Included in User Story 1 (GET /todos/{id} endpoint)

### Within Each Phase

**Phase 2 (Foundational)**:
- T009 (config) before T010 (database) - database needs config
- T010 (database) before T011 (models) - models need database setup
- T011 (models) before T012 (auth) - auth can run in parallel with models
- T013 (test fixtures) before T014-T017 (auth tests)
- T018 (main app) after T012 (auth) - main needs auth dependency

**Phase 3 (User Story 1)**:
- T020-T024 (CRUD operations) can all run in parallel - different functions
- T025-T029 (endpoints) depend on T020-T024 (CRUD) - endpoints use CRUD functions
- T030 (register router) depends on T025-T029 (endpoints)
- T031-T039 (tests) can run in parallel after T030 - different test functions

**Phase 4 (User Story 3)**:
- T040-T041 (filtering logic) can run in parallel - different parameters
- T042 (update endpoint) depends on T040-T041
- T043-T047 (tests) can run in parallel after T042

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005, T006, T007, T008 can all run in parallel

**Phase 2 (Foundational)**:
- T014, T015, T016, T017 (auth tests) can run in parallel

**Phase 3 (User Story 1)**:
- T020, T021, T022, T023, T024 (CRUD functions) can run in parallel
- T031, T032, T033, T034, T035, T036, T037, T038, T039 (tests) can run in parallel

**Phase 4 (User Story 3)**:
- T040, T041 (filtering parameters) can run in parallel
- T043, T044, T045, T046, T047 (tests) can run in parallel

**Phase 5 (Polish)**:
- T048, T049, T052, T053 can run in parallel

---

## Parallel Example: User Story 1 CRUD Operations

```bash
# Launch all CRUD functions together:
Task: "Implement get_todos_by_user in backend/app/crud.py"
Task: "Implement get_todo_by_id in backend/app/crud.py"
Task: "Implement create_todo in backend/app/crud.py"
Task: "Implement update_todo in backend/app/crud.py"
Task: "Implement delete_todo in backend/app/crud.py"

# After CRUD is done, launch all tests together:
Task: "Write test_create_todo in backend/tests/test_todos.py"
Task: "Write test_list_todos in backend/tests/test_todos.py"
Task: "Write test_get_todo in backend/tests/test_todos.py"
Task: "Write test_update_todo in backend/tests/test_todos.py"
Task: "Write test_delete_todo in backend/tests/test_todos.py"
Task: "Write test_user_isolation in backend/tests/test_isolation.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T019) - CRITICAL, includes JWT auth
3. Complete Phase 3: User Story 1 (T020-T039) - Complete CRUD with user isolation
4. **STOP and VALIDATE**: Test User Story 1 independently with pytest
5. Deploy/demo if ready - this is a functional todo API

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (JWT auth working)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - full CRUD!)
3. Add User Story 3 → Test independently → Deploy/Demo (Enhanced with filtering)
4. Polish → Final touches → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T019)
2. Once Foundational is done:
   - Developer A: User Story 1 CRUD operations (T020-T024)
   - Developer B: User Story 1 endpoints (T025-T030, depends on A)
   - Developer C: User Story 1 tests (T031-T039, depends on B)
   - Developer D: User Story 3 (T040-T047, can start after Foundational)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 53

**By Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 11 tasks (includes US2 - JWT Authentication)
- Phase 3 (User Story 1 - CRUD): 20 tasks
- Phase 4 (User Story 3 - Filtering): 8 tasks
- Phase 5 (Polish): 6 tasks

**By User Story**:
- US1 (Create and Manage Todos - P1): 20 tasks
- US2 (JWT Authentication - P1): 7 tasks (in Foundational phase)
- US3 (Filter and Query - P2): 8 tasks
- US4 (Get by ID - P2): Included in US1 (T021, T027, T033, T034)

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 = 39 tasks for complete CRUD API with JWT authentication

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- US2 (JWT Authentication) is in Foundational phase as it's required for all endpoints
- US4 (Get by ID) is integrated into US1 as it's part of basic CRUD
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests use in-memory SQLite, no external database needed
- All endpoints require JWT authentication (enforced by dependency)
