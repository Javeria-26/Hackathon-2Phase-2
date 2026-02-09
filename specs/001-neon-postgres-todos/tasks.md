# Tasks: Neon PostgreSQL Todo Data Layer

**Input**: Design documents from `/specs/001-neon-postgres-todos/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are not included. Existing test files (test_todos.py, test_isolation.py) will be used for validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for application code
- **Tests**: `backend/tests/` for test files
- **Config**: `backend/` for configuration files

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management

- [ ] T001 Add asyncpg==0.29.0 to backend/requirements.txt for PostgreSQL async driver
- [ ] T002 Install dependencies from backend/requirements.txt using pip
- [ ] T003 Create backend/.env.example with Neon PostgreSQL connection string template
- [ ] T004 Update backend/.env with actual Neon DATABASE_URL (postgresql+asyncpg://...)

**Checkpoint**: Dependencies installed, environment configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Update backend/app/config.py to load DATABASE_URL from environment
- [ ] T006 Update backend/app/database.py with Neon-specific connection pooling (pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=3600)
- [ ] T007 Update backend/app/database.py to use postgresql+asyncpg:// connection string with SSL
- [ ] T008 Verify backend/app/database.py async session factory and get_session() dependency
- [ ] T009 Verify backend/app/database.py create_db_and_tables() function for schema creation
- [ ] T010 Update backend/app/main.py startup event to call create_db_and_tables()

**Checkpoint**: Foundation ready - Neon PostgreSQL connection established, session management configured, schema creation ready

---

## Phase 3: User Story 1 - Persist User Todo Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement CRUD operations for todo tasks with reliable persistence across database connection cycles

**Independent Test**: Create a todo task, restart the database connection, and verify the task still exists with all its attributes intact

### Implementation for User Story 1

- [ ] T011 [P] [US1] Update Todo model in backend/app/models.py with UUID primary key (id field with uuid.uuid4() default_factory)
- [ ] T012 [P] [US1] Update Todo model in backend/app/models.py with user_id field (indexed, nullable=False)
- [ ] T013 [P] [US1] Update Todo model in backend/app/models.py with title field (min_length=1, max_length=500, nullable=False)
- [ ] T014 [P] [US1] Update Todo model in backend/app/models.py with description field (default="", max_length=5000)
- [ ] T015 [P] [US1] Update Todo model in backend/app/models.py with completed field (default=False, nullable=False)
- [ ] T016 [P] [US1] Update Todo model in backend/app/models.py with created_at and updated_at timestamp fields
- [ ] T017 [US1] Add field validator to Todo model in backend/app/models.py for title (not empty, strip whitespace)
- [ ] T018 [US1] Add field validator to Todo model in backend/app/models.py for description (strip whitespace)
- [ ] T019 [US1] Implement create_todo() function in backend/app/crud.py with user_id parameter
- [ ] T020 [US1] Implement get_todos() function in backend/app/crud.py with user_id, skip, limit parameters (ordered by created_at DESC)
- [ ] T021 [US1] Implement get_todo() function in backend/app/crud.py with user_id and todo_id parameters
- [ ] T022 [US1] Implement update_todo() function in backend/app/crud.py with user_id, todo_id, and todo_data parameters
- [ ] T023 [US1] Implement delete_todo() function in backend/app/crud.py with user_id and todo_id parameters
- [ ] T024 [US1] Implement mark_complete() helper function in backend/app/crud.py with user_id, todo_id, completed parameters
- [ ] T025 [US1] Add error handling for database connection failures in backend/app/crud.py
- [ ] T026 [US1] Add error handling for validation errors in backend/app/crud.py

**Checkpoint**: User Story 1 complete - CRUD operations work, tasks persist across connection cycles

---

## Phase 4: User Story 2 - Enforce User Data Isolation (Priority: P1)

**Goal**: Ensure all database operations enforce user-level data isolation to prevent cross-user data access

**Independent Test**: Create tasks for two different users, then query each user's tasks and verify that only their own tasks are returned, never the other user's tasks

### Implementation for User Story 2

- [ ] T027 [US2] Verify create_todo() in backend/app/crud.py filters by user_id (sets user_id on new task)
- [ ] T028 [US2] Verify get_todos() in backend/app/crud.py filters by user_id (WHERE user_id = ?)
- [ ] T029 [US2] Verify get_todo() in backend/app/crud.py filters by both id AND user_id
- [ ] T030 [US2] Verify update_todo() in backend/app/crud.py filters by both id AND user_id (returns None if not owned)
- [ ] T031 [US2] Verify delete_todo() in backend/app/crud.py filters by both id AND user_id (returns False if not owned)
- [ ] T032 [US2] Verify mark_complete() in backend/app/crud.py filters by both id AND user_id
- [ ] T033 [US2] Add user_id validation in backend/app/crud.py (ensure user_id is not None or empty)
- [ ] T034 [US2] Update backend/app/models.py to add composite index on (user_id, created_at) for optimized queries

**Checkpoint**: User Story 2 complete - All operations enforce user isolation, zero cross-user data access possible

---

## Phase 5: User Story 3 - Handle Concurrent Operations (Priority: P2)

**Goal**: Support multiple users simultaneously creating, reading, updating, and deleting their own tasks without data corruption or conflicts

**Independent Test**: Simulate multiple concurrent database operations (creates, updates, deletes) from different users and verify all operations complete successfully without data loss or corruption

### Implementation for User Story 3

- [ ] T035 [US3] Verify connection pooling parameters in backend/app/database.py support concurrent operations (pool_size=5, max_overflow=10)
- [ ] T036 [US3] Verify pool_pre_ping=True in backend/app/database.py to detect stale connections
- [ ] T037 [US3] Verify pool_recycle=3600 in backend/app/database.py to prevent idle connection timeouts
- [ ] T038 [US3] Add connection retry logic in backend/app/database.py for transient failures
- [ ] T039 [US3] Verify PostgreSQL isolation level (READ COMMITTED) is appropriate for concurrent operations
- [ ] T040 [US3] Add connection timeout handling in backend/app/database.py
- [ ] T041 [US3] Create backend/tests/test_concurrent.py for concurrent operation validation (manual testing)

**Checkpoint**: User Story 3 complete - System handles 100+ concurrent operations without corruption

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T042 [P] Update backend/README.md with Neon PostgreSQL setup instructions
- [ ] T043 [P] Verify backend/.env.example has all required environment variables documented
- [ ] T044 Verify all CRUD operations in backend/app/crud.py have proper error handling
- [ ] T045 Verify all field validators in backend/app/models.py work correctly
- [ ] T046 Run manual validation using backend/tests/test_todos.py to verify CRUD operations
- [ ] T047 Run manual validation using backend/tests/test_isolation.py to verify user isolation
- [ ] T048 Run manual validation using backend/tests/test_concurrent.py to verify concurrent operations
- [ ] T049 Verify database schema created successfully with all indexes (user_id, composite)
- [ ] T050 Verify query performance meets <100ms target for 1000 tasks per user
- [ ] T051 Run quickstart.md validation steps to ensure setup guide is accurate

**Checkpoint**: All polish tasks complete, system ready for integration with API layer

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P1): Depends on User Story 1 completion (validates US1 implementation)
  - User Story 3 (P2): Can start after Foundational - No dependencies on other stories (but benefits from US1 being complete for testing)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 1 completion - Validates and enforces isolation in US1 CRUD operations
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent of US1/US2 but concurrent testing requires CRUD operations from US1

### Within Each User Story

- **User Story 1**: Model fields can be updated in parallel (T011-T018), then validators (T017-T018), then CRUD operations sequentially (T019-T024), then error handling (T025-T026)
- **User Story 2**: All verification tasks can run in parallel once US1 is complete
- **User Story 3**: All verification tasks can run in parallel once Foundational is complete

### Parallel Opportunities

- **Setup Phase**: T001-T004 can run in parallel (different files)
- **Foundational Phase**: T005-T010 must run sequentially (same files, dependencies)
- **User Story 1 Models**: T011-T016 can run in parallel (different fields in same file, but independent changes)
- **User Story 2**: T027-T034 can run in parallel (verification tasks)
- **User Story 3**: T035-T041 can run in parallel (verification tasks)
- **Polish Phase**: T042-T043 can run in parallel (different files)

---

## Parallel Example: User Story 1 Models

```bash
# Launch all model field updates together:
Task: "Update Todo model with UUID primary key in backend/app/models.py"
Task: "Update Todo model with user_id field in backend/app/models.py"
Task: "Update Todo model with title field in backend/app/models.py"
Task: "Update Todo model with description field in backend/app/models.py"
Task: "Update Todo model with completed field in backend/app/models.py"
Task: "Update Todo model with timestamp fields in backend/app/models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T010) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T011-T026)
4. **STOP and VALIDATE**: Test User Story 1 independently using existing test_todos.py
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational (T001-T010) → Foundation ready
2. Add User Story 1 (T011-T026) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (T027-T034) → Test independently → Deploy/Demo (Isolation enforced!)
4. Add User Story 3 (T035-T041) → Test independently → Deploy/Demo (Concurrent support!)
5. Add Polish (T042-T051) → Final validation → Production ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T010)
2. Once Foundational is done:
   - Developer A: User Story 1 (T011-T026)
   - Developer B: User Story 3 (T035-T041) - Can start in parallel
3. After US1 complete:
   - Developer A or B: User Story 2 (T027-T034) - Validates US1
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 51
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (User Story 1): 16 tasks
- Phase 4 (User Story 2): 8 tasks
- Phase 5 (User Story 3): 7 tasks
- Phase 6 (Polish): 10 tasks

**Parallel Opportunities**: 15 tasks marked [P]
- Setup: 4 tasks (T001-T004)
- User Story 1 Models: 6 tasks (T011-T016)
- Polish: 2 tasks (T042-T043)

**User Story Breakdown**:
- US1 (Persist): 16 tasks - Core CRUD implementation
- US2 (Isolation): 8 tasks - User isolation enforcement
- US3 (Concurrent): 7 tasks - Concurrent operation support

**Independent Test Criteria**:
- US1: Create task, restart connection, verify persistence
- US2: Create tasks for 2 users, verify isolation
- US3: Run 100+ concurrent operations, verify no corruption

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 26 tasks

---

## Notes

- [P] tasks = different files or independent changes, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included as they were not explicitly requested in spec
- Existing test files (test_todos.py, test_isolation.py, test_concurrent.py) will be used for manual validation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
