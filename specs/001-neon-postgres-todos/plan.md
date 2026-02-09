# Implementation Plan: Neon PostgreSQL Todo Data Layer

**Branch**: `001-neon-postgres-todos` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-neon-postgres-todos/spec.md`

## Summary

Implement a PostgreSQL data persistence layer using Neon Serverless PostgreSQL and SQLModel ORM to store user-scoped todo tasks. The system must enforce strict user-level data isolation, support concurrent operations, and provide reliable persistence across database connection cycles. This plan focuses exclusively on the database schema, models, and connection management - API endpoints and authentication are handled by separate specifications.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: SQLModel 0.0.14, asyncpg (PostgreSQL async driver), SQLAlchemy 2.0+
**Storage**: Neon Serverless PostgreSQL with connection pooling
**Testing**: pytest 7.4+, pytest-asyncio 0.23+, httpx 0.26+ for integration tests
**Target Platform**: Linux server (FastAPI backend)
**Project Type**: Web application (backend component)
**Performance Goals**: <100ms query latency for user task lists (up to 1000 tasks), 100+ concurrent operations
**Constraints**: Serverless-safe connection patterns, connection pooling required, <200ms p95 latency
**Scale/Scope**: Multi-user application, user-scoped data isolation, CRUD operations on todo tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Security-First Design ✅
- **Data Isolation**: All database queries filter by user_id (enforced at model/CRUD layer)
- **No Cross-User Access**: Foreign key constraints and query patterns prevent data leakage
- **Referential Integrity**: user_id references authentication system's user table
- **Input Validation**: Field length limits (title: 500 chars, description: 5000 chars) enforced at model level

### Clear Separation of Concerns ✅
- **Database Spec Boundaries**: This spec handles ONLY schema, models, and persistence
- **No API Logic**: Endpoint definitions handled by Backend Spec (Phase III)
- **No Authentication**: User identity provided by Authentication Spec (Phase I)
- **Interface**: Exposes CRUD functions that accept user_id parameter

### Production-Ready Architecture ✅
- **Error Handling**: Database connection failures raise clear exceptions
- **Serverless Patterns**: Connection pooling with pool_pre_ping, pool_recycle
- **Configuration**: DATABASE_URL via environment variables (.env)
- **Graceful Degradation**: Connection retry logic, timeout handling

### Minimal Viable Changes ✅
- **Scope**: Only database layer - no API, no UI, no authentication logic
- **No Speculation**: No soft deletes, no audit logs, no advanced features
- **Smallest Diff**: Leverage existing SQLModel patterns, minimal abstraction

### Technology Standards ✅
- **Database**: Neon Serverless PostgreSQL (as specified)
- **ORM**: SQLModel (as specified)
- **Async Driver**: asyncpg (PostgreSQL standard for async Python)
- **Connection Management**: SQLAlchemy async engine with pooling

### Spec-Driven Development ✅
- **Specification**: spec.md defines all requirements and boundaries
- **Plan**: This document (plan.md) defines architecture and decisions
- **Tasks**: Will be generated via /sp.tasks after plan approval
- **Traceability**: All implementation references spec requirements

**Gate Status**: ✅ PASS - All constitutional requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-neon-postgres-todos/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (architectural plan)
├── research.md          # Phase 0: Neon PostgreSQL research
├── data-model.md        # Phase 1: Database schema and models
├── quickstart.md        # Phase 1: Setup and configuration guide
├── contracts/           # Phase 1: Database operation contracts
│   └── crud-operations.md
└── tasks.md             # Phase 2: Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models.py           # SQLModel definitions (Todo, TodoBase, etc.)
│   ├── database.py         # Database engine, session management
│   ├── crud.py             # CRUD operations with user_id filtering
│   ├── config.py           # Settings (DATABASE_URL, etc.)
│   └── routers/
│       └── todos.py        # API endpoints (out of scope for this spec)
├── tests/
│   ├── conftest.py         # Test fixtures (database session, test data)
│   ├── test_isolation.py   # User isolation tests
│   ├── test_todos.py       # CRUD operation tests
│   └── test_concurrent.py  # Concurrent operation tests (new)
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
└── README.md              # Backend documentation
```

**Structure Decision**: Using existing backend/ directory structure. This spec focuses on the database layer components (models.py, database.py, crud.py) within the established FastAPI backend architecture.

## Complexity Tracking

> **No violations detected - this section intentionally left empty**

All architectural decisions align with constitutional principles. No additional complexity introduced beyond what is necessary for the specified requirements.

---

## Phase 0: Research & Technology Decisions

### Research Areas

1. **Neon PostgreSQL Connection Patterns**
   - Serverless-specific connection string format
   - Connection pooling best practices for Neon
   - SSL/TLS requirements
   - Connection lifecycle management

2. **SQLModel + PostgreSQL Integration**
   - Async driver selection (asyncpg vs psycopg3)
   - SQLAlchemy 2.0 compatibility
   - Migration from SQLite to PostgreSQL
   - Type mapping differences

3. **Index Strategy**
   - Composite index on (user_id, created_at) for efficient queries
   - Index on user_id alone for filtering
   - UUID vs integer primary keys performance

4. **Concurrent Operation Handling**
   - Transaction isolation levels
   - Optimistic vs pessimistic locking
   - Connection pool sizing for concurrent users

### Key Decisions

**Decision 1: Async Driver - asyncpg**
- **Rationale**: asyncpg is the fastest and most mature async PostgreSQL driver for Python. Native support in SQLAlchemy 2.0, excellent performance for serverless environments.
- **Alternatives Considered**:
  - psycopg3: Newer but less mature, slightly slower
  - psycopg2: Synchronous only, not suitable for async FastAPI
- **Implementation**: Use `postgresql+asyncpg://` connection string prefix

**Decision 2: Connection Pooling Strategy**
- **Rationale**: Neon serverless requires careful connection management. Use pool_pre_ping to verify connections, pool_recycle to prevent stale connections.
- **Parameters**:
  - pool_size=5 (base connections)
  - max_overflow=10 (burst capacity)
  - pool_recycle=3600 (1 hour, prevents Neon idle timeout)
  - pool_pre_ping=True (verify before use)
- **Alternatives Considered**:
  - No pooling: Too slow, creates new connection per request
  - Larger pool: Wastes connections in serverless environment

**Decision 3: Primary Key Strategy - UUID**
- **Rationale**: UUIDs prevent ID enumeration attacks, work well in distributed systems, no collision risk with concurrent inserts.
- **Implementation**: Use Python's uuid.uuid4() as default_factory
- **Alternatives Considered**:
  - Auto-increment integers: Predictable, enables enumeration attacks
  - ULID: More complex, no significant benefit for this use case

**Decision 4: Index Strategy**
- **Rationale**: Most queries filter by user_id and order by created_at. Composite index optimizes the common query pattern.
- **Indexes**:
  - Primary: id (UUID, automatic)
  - Secondary: user_id (single column, for user filtering)
  - Composite: (user_id, created_at) (for ordered user queries)
- **Alternatives Considered**:
  - Single user_id index: Slower for ordered queries
  - Full-text search indexes: Out of scope per spec

**Decision 5: Migration Strategy - Schema Recreation**
- **Rationale**: This is a new Neon PostgreSQL setup, not a production migration. Use SQLModel.metadata.create_all() for initial schema creation.
- **Implementation**: create_db_and_tables() function called on startup
- **Alternatives Considered**:
  - Alembic migrations: Overkill for initial setup, add later if needed
  - Manual SQL: Less maintainable, SQLModel handles it

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete schema definition.

**Summary**:
- **Todo Table**: id (UUID PK), user_id (indexed FK), title (varchar 500), description (varchar 5000), completed (boolean), created_at (timestamp), updated_at (timestamp)
- **Indexes**: Primary on id, secondary on user_id, composite on (user_id, created_at)
- **Constraints**: NOT NULL on user_id, title; CHECK on title length; DEFAULT false on completed
- **Relationships**: user_id references users table (managed by auth system)

### API Contracts

See [contracts/crud-operations.md](./contracts/crud-operations.md) for complete interface definition.

**CRUD Operations** (all require user_id parameter):
- `create_todo(session, user_id, todo_data)` → Todo
- `get_todos(session, user_id, skip, limit)` → List[Todo]
- `get_todo(session, user_id, todo_id)` → Todo | None
- `update_todo(session, user_id, todo_id, todo_data)` → Todo | None
- `delete_todo(session, user_id, todo_id)` → bool
- `mark_complete(session, user_id, todo_id, completed)` → Todo | None

**Isolation Guarantee**: All operations filter by user_id. No operation can access or modify tasks belonging to other users.

### Configuration

See [quickstart.md](./quickstart.md) for setup instructions.

**Environment Variables**:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:3000
```

**Neon Connection String Format**:
- Protocol: `postgresql+asyncpg://`
- SSL: `?sslmode=require` (mandatory for Neon)
- Pooling: Configured in database.py engine creation

---

## Phase 2: Implementation Roadmap

**Note**: Detailed tasks will be generated via `/sp.tasks` command. This section provides high-level implementation phases.

### Implementation Phases

**Phase 2.1: Database Connection Setup**
- Configure Neon PostgreSQL connection string
- Set up async engine with serverless-safe pooling
- Implement session management with dependency injection
- Add connection error handling and retry logic

**Phase 2.2: Schema & Models**
- Define Todo SQLModel with all required fields
- Add field validators (title not empty, length limits)
- Configure indexes (user_id, composite user_id+created_at)
- Implement schema creation on startup

**Phase 2.3: CRUD Operations**
- Implement create_todo with user_id enforcement
- Implement get_todos with user filtering and ordering
- Implement get_todo with user ownership validation
- Implement update_todo with user authorization check
- Implement delete_todo with user authorization check
- Implement mark_complete helper function

**Phase 2.4: Testing & Validation**
- Write unit tests for each CRUD operation
- Write integration tests for user isolation
- Write concurrent operation tests (100+ simultaneous ops)
- Validate query performance (<100ms for 1000 tasks)
- Test edge cases (invalid user_id, missing fields, etc.)

### Success Validation

Each phase must pass these checks before proceeding:

**Phase 2.1 Validation**:
- [ ] Database connection established successfully
- [ ] Connection pool configured with correct parameters
- [ ] SSL connection to Neon verified
- [ ] Connection error handling tested

**Phase 2.2 Validation**:
- [ ] Todo table created with correct schema
- [ ] All indexes created (user_id, composite)
- [ ] Field validators working (title, description lengths)
- [ ] Timestamps auto-populate correctly

**Phase 2.3 Validation**:
- [ ] All CRUD operations filter by user_id
- [ ] No operation can access other users' data
- [ ] Queries return results ordered by created_at
- [ ] Update operations validate ownership

**Phase 2.4 Validation**:
- [ ] All tests pass (unit, integration, concurrent)
- [ ] Zero cross-user data leakage in tests
- [ ] Query performance meets <100ms target
- [ ] 100+ concurrent operations succeed without corruption

---

## Risk Analysis

### Risk 1: Neon Connection Limits
**Impact**: High | **Probability**: Medium
**Description**: Neon free tier has connection limits. Excessive connections could cause failures.
**Mitigation**:
- Use connection pooling (pool_size=5, max_overflow=10)
- Implement pool_pre_ping to detect stale connections
- Monitor connection usage in production
- Upgrade Neon tier if limits reached

### Risk 2: Migration from SQLite
**Impact**: Medium | **Probability**: Low
**Description**: Existing SQLite database (todos.db) contains test data that needs migration.
**Mitigation**:
- This is development data, not production
- No migration needed - fresh Neon database
- Document that existing SQLite data is for local testing only
- Keep SQLite for local development, Neon for production

### Risk 3: Concurrent Write Conflicts
**Impact**: Medium | **Probability**: Low
**Description**: Multiple users updating same task simultaneously could cause conflicts.
**Mitigation**:
- PostgreSQL default isolation level (READ COMMITTED) handles this
- Last write wins (acceptable for todo app)
- No optimistic locking needed for this use case
- Monitor for actual conflicts in testing

### Risk 4: Query Performance Degradation
**Impact**: Medium | **Probability**: Low
**Description**: Query performance could degrade with large numbers of tasks per user.
**Mitigation**:
- Composite index on (user_id, created_at) optimizes common query
- Pagination support (skip/limit parameters)
- Performance tests validate <100ms for 1000 tasks
- Monitor query plans in production

---

## Dependencies

### External Dependencies
- **Neon PostgreSQL**: Serverless PostgreSQL instance must be provisioned
- **Authentication System (Phase I)**: Provides valid user_id values
- **Environment Configuration**: DATABASE_URL must be configured

### Internal Dependencies
- **SQLModel**: Already in requirements.txt (0.0.14)
- **asyncpg**: Must be added to requirements.txt
- **SQLAlchemy**: Dependency of SQLModel (2.0+)

### Dependency Installation
```bash
pip install asyncpg==0.29.0
```

---

## Architectural Decision Records (ADRs)

The following decisions meet the three-part test for ADR documentation:

### ADR Candidates

**1. Choice of asyncpg over psycopg3**
- **Impact**: Long-term (affects all database operations)
- **Alternatives**: Yes (psycopg3, psycopg2)
- **Scope**: Cross-cutting (all database interactions)
- **Recommendation**: Document with `/sp.adr asyncpg-driver-selection`

**2. UUID Primary Keys vs Auto-Increment**
- **Impact**: Long-term (affects data model, cannot easily change)
- **Alternatives**: Yes (integer auto-increment, ULID)
- **Scope**: Cross-cutting (affects all tables, API responses)
- **Recommendation**: Document with `/sp.adr uuid-primary-keys`

**3. Connection Pooling Strategy for Neon Serverless**
- **Impact**: Long-term (affects performance and reliability)
- **Alternatives**: Yes (no pooling, larger pool, external pooler)
- **Scope**: Cross-cutting (affects all database operations)
- **Recommendation**: Document with `/sp.adr neon-connection-pooling`

---

## Next Steps

1. **Review this plan**: Ensure architectural decisions align with project goals
2. **Create ADRs**: Document the three significant decisions identified above
3. **Generate tasks**: Run `/sp.tasks` to create implementation task list
4. **Begin implementation**: Execute tasks via `/sp.implement`

---

## Appendix: Constitution Compliance Matrix

| Constitutional Principle | Compliance Status | Evidence |
|-------------------------|-------------------|----------|
| Spec-Driven Development | ✅ PASS | spec.md → plan.md → tasks.md workflow |
| Zero Manual Coding | ✅ PASS | All code via Claude Code agentic workflow |
| Security-First Design | ✅ PASS | User isolation enforced at all query levels |
| Clear Separation of Concerns | ✅ PASS | Database layer only, no API/auth logic |
| Production-Ready Architecture | ✅ PASS | Connection pooling, error handling, config |
| Minimal Viable Changes | ✅ PASS | Only specified features, no scope creep |
| Technology Standards | ✅ PASS | Neon PostgreSQL + SQLModel as specified |
| API Contract Standards | ✅ PASS | CRUD operations documented in contracts/ |
| Data Standards | ✅ PASS | user_id filtering, indexes, constraints |

**Overall Compliance**: ✅ FULL COMPLIANCE - Ready for task generation
