# Implementation Plan: FastAPI Todo Backend

**Branch**: `003-fastapi-todo-backend` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-fastapi-todo-backend/spec.md`

## Summary

Implement a secure FastAPI backend service that provides REST API endpoints for user-scoped todo management. The service verifies JWT tokens issued by Better Auth, extracts authenticated user identity, and enforces strict data isolation to ensure users can only access their own todos. All data is persisted to Neon PostgreSQL using SQLModel ORM with async operations.

**Technical Approach**: Async FastAPI with python-jose for JWT verification, SQLModel with asyncpg for database operations, and comprehensive error handling with proper HTTP status codes.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, SQLModel 0.0.14, python-jose 3.3.0, asyncpg 0.29.0
**Storage**: Neon PostgreSQL (serverless) with SQLModel ORM
**Testing**: pytest with pytest-asyncio and httpx TestClient
**Target Platform**: Linux/Windows server (containerizable)
**Project Type**: Web API (backend only)
**Performance Goals**: <200ms response time for queries up to 1000 todos, 100+ concurrent requests
**Constraints**: Stateless design, serverless-compatible connection patterns, JWT verification on all endpoints
**Scale/Scope**: Multi-user system with user-scoped data isolation, 5 REST endpoints, single database table

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Security-First Design ✅ PASS
- **JWT Verification**: All endpoints require valid JWT token from Better Auth
- **User Extraction**: User ID extracted from JWT claims (`sub` or `userId`)
- **Authorization**: Database queries filtered by authenticated user ID
- **Data Isolation**: Users cannot access other users' todos (403 Forbidden)
- **No Hardcoded Secrets**: JWT secret and database URL from environment variables

### Clear Separation of Concerns ✅ PASS
- **Backend Spec Boundaries**: Stateless API service, no frontend logic
- **Interface Contract**: REST API with documented endpoints and response formats
- **Dependencies**: Better Auth (JWT issuer), Neon PostgreSQL (data store), Frontend (API consumer)
- **No Internal Assumptions**: Uses documented JWT claims, standard REST conventions

### Production-Ready Architecture ✅ PASS
- **Error Handling**: Comprehensive exception handlers with clear error messages
- **HTTP Status Codes**: Proper codes for all scenarios (200, 201, 400, 401, 403, 404, 422, 500, 503)
- **Input Validation**: Pydantic models with field validators
- **Connection Pooling**: Configured for Neon serverless environment
- **Graceful Degradation**: Database connection errors return 503 with message

### Minimal Viable Changes ✅ PASS
- **Scope Adherence**: Only implements specified CRUD endpoints and JWT verification
- **No Speculative Features**: No rate limiting, API versioning, or pagination (out of scope)
- **Focused Implementation**: Single database table, straightforward REST patterns

### API Contract Standards ✅ PASS
- **Endpoint Structure**: `/todos` (list, create), `/todos/{id}` (get, update, delete)
- **Authentication**: `Authorization: Bearer <token>` header required
- **Request/Response**: JSON format with proper validation
- **Status Codes**: Follows constitution standards

### Technology Standards ✅ PASS
- **Backend Stack**: Python FastAPI, SQLModel, JWT verification
- **Database**: Neon PostgreSQL with serverless-safe patterns
- **No Unapproved Dependencies**: All libraries align with constitution

**Constitution Compliance**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/003-fastapi-todo-backend/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Technical research and patterns
├── data-model.md        # Database schema and entities
├── quickstart.md        # Setup and running instructions
├── contracts/           # API contracts
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization, CORS, lifespan
│   ├── config.py            # Pydantic Settings for environment config
│   ├── database.py          # Async engine, session factory, table creation
│   ├── models.py            # SQLModel models (Todo, TodoCreate, TodoUpdate, TodoResponse)
│   ├── auth.py              # JWT verification dependency (verify_token, get_current_user_id)
│   ├── crud.py              # Database operations (get_todos_by_user, create_todo, etc.)
│   └── routers/
│       ├── __init__.py
│       └── todos.py         # Todo REST endpoints (5 routes)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures (client, session, auth_token, auth_headers)
│   ├── test_auth.py         # JWT verification tests (missing, invalid, expired, valid tokens)
│   ├── test_todos.py        # CRUD tests (create, list, get, update, delete)
│   └── test_isolation.py    # User isolation tests (403 for other users' todos)
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template with placeholders
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # Setup and API documentation
```

**Structure Decision**: Single backend project with modular organization. The `app/` directory contains all application code organized by concern (config, database, models, auth, crud, routers). Tests mirror the application structure. This follows FastAPI best practices and keeps the codebase maintainable for a hackathon demo.

## Complexity Tracking

No constitution violations. All requirements align with established principles.

## Phase 0: Research ✅ COMPLETE

**Status**: Research completed by agent (see `research.md`)

**Key Findings**:
1. **JWT Verification**: Use python-jose with HS256, check both `sub` and `userId` claims for Better Auth compatibility
2. **Database**: Async SQLModel with asyncpg driver, connection pooling (5-10 connections) for Neon serverless
3. **Connection String**: `postgresql+asyncpg://...?sslmode=require` (SSL required for Neon)
4. **Testing**: pytest with in-memory SQLite, mock JWT tokens with jose library
5. **Error Handling**: Global exception handlers for validation errors and JWT errors

**Decisions Made**:
- **JWT Library**: python-jose (most widely adopted in FastAPI ecosystem)
- **Database Driver**: asyncpg (async support, best performance for PostgreSQL)
- **ORM Pattern**: Async SQLModel with async sessions
- **Testing Database**: In-memory SQLite (fast, isolated tests)
- **CORS Configuration**: Specific origin with credentials enabled

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete schema definition.

**Summary**:
- **Todo Entity**: id (UUID), user_id (string, indexed), title (string, 1-200 chars), description (string, 0-1000 chars), completed (boolean), created_at (timestamp), updated_at (timestamp)
- **Relationships**: Each todo belongs to exactly one user (user_id foreign key concept)
- **Indexes**: user_id indexed for fast user-scoped queries
- **Validation**: Title required and non-empty, description optional, length limits enforced

### API Contracts

See [contracts/openapi.yaml](./contracts/openapi.yaml) for complete OpenAPI specification.

**Endpoints**:
1. `POST /todos` - Create new todo (201 Created)
2. `GET /todos` - List user's todos with optional filters (200 OK)
3. `GET /todos/{id}` - Get specific todo (200 OK, 404 Not Found, 403 Forbidden)
4. `PUT /todos/{id}` - Update todo (200 OK, 404 Not Found, 403 Forbidden)
5. `DELETE /todos/{id}` - Delete todo (204 No Content, 404 Not Found, 403 Forbidden)

**Authentication**: All endpoints require `Authorization: Bearer <jwt_token>` header

**Query Parameters**:
- `completed` (boolean, optional): Filter by completion status
- `search` (string, optional): Search in title and description (case-insensitive)

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup instructions.

## Phase 2: Implementation Tasks

**Note**: Tasks will be generated by `/sp.tasks` command after this plan is approved.

**Expected Task Categories**:
1. **Project Setup**: Create directory structure, requirements.txt, .env.example
2. **Configuration**: Implement config.py with Pydantic Settings
3. **Database Layer**: Implement database.py with async engine and session management
4. **Models**: Implement SQLModel models with validation
5. **Authentication**: Implement JWT verification dependency
6. **CRUD Operations**: Implement database operations in crud.py
7. **API Routes**: Implement 5 REST endpoints in routers/todos.py
8. **Error Handling**: Implement global exception handlers
9. **CORS Configuration**: Configure CORS middleware
10. **Testing**: Implement test fixtures and test cases
11. **Documentation**: Create README with API documentation

## Architecture Decisions

### 1. Async vs Sync Database Operations

**Decision**: Use async SQLModel with asyncpg

**Rationale**:
- Better performance for I/O-bound operations (database queries)
- Non-blocking operations allow handling more concurrent requests
- FastAPI is async-first, aligns with framework design
- Neon PostgreSQL works well with async drivers

**Alternatives Considered**:
- Sync SQLModel: Simpler but blocks on database operations, lower throughput
- Raw asyncpg: More control but loses ORM benefits and type safety

### 2. JWT Claim for User ID

**Decision**: Check both `sub` (standard) and `userId` (Better Auth custom) claims

**Rationale**:
- Better Auth may use either claim depending on configuration
- Checking both ensures maximum compatibility
- Fallback pattern is safe and explicit

**Alternatives Considered**:
- Only check `sub`: May miss Better Auth tokens using `userId`
- Only check `userId`: Violates JWT standard, less portable

### 3. Database Connection Pooling

**Decision**: Pool size 5-10 with `pool_pre_ping=True`

**Rationale**:
- Neon serverless may close idle connections
- `pool_pre_ping` verifies connections before use
- Moderate pool size balances performance and resource usage
- Suitable for hackathon demo scale

**Alternatives Considered**:
- Large pool (20+): Wastes resources in serverless environment
- No pooling: Poor performance, connection overhead on every request

### 4. Error Response Format

**Decision**: Consistent JSON error format with `error.code` and `error.message`

**Rationale**:
- Frontend can parse errors consistently
- Provides both machine-readable code and human-readable message
- Aligns with REST API best practices

**Example**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {"title": "Field required"}
  }
}
```

### 5. User Isolation Strategy

**Decision**: Filter all database queries by authenticated user_id from JWT

**Rationale**:
- Enforces data isolation at database query level
- Prevents accidental cross-user data leakage
- Simple and explicit pattern

**Implementation**:
- Extract user_id from JWT in auth dependency
- Pass user_id to all CRUD operations
- Add `WHERE user_id = ?` to all queries

### 6. Testing Strategy

**Decision**: In-memory SQLite for tests, mock JWT tokens

**Rationale**:
- Fast test execution (no external database)
- Isolated tests (each test gets fresh database)
- Easy to set up and tear down
- Mock JWT tokens allow testing auth without real tokens

**Alternatives Considered**:
- Test against real Neon database: Slower, requires network, harder to isolate
- Mock database layer: Loses integration testing value

## Risk Analysis

### Risk 1: JWT Secret Mismatch

**Description**: Backend JWT secret doesn't match frontend Better Auth secret

**Impact**: All authentication fails, API unusable

**Mitigation**:
- Document requirement clearly in .env.example
- Add startup validation to check JWT_SECRET_KEY is set
- Test with real frontend JWT token during integration

**Likelihood**: Medium | **Severity**: High

### Risk 2: Database Connection Issues

**Description**: Neon PostgreSQL connection fails or times out

**Impact**: API returns 503 errors, no data persistence

**Mitigation**:
- Use `pool_pre_ping=True` to verify connections
- Implement proper error handling with 503 status
- Add database health check endpoint
- Test connection on startup

**Likelihood**: Low | **Severity**: High

### Risk 3: User Isolation Bugs

**Description**: Query doesn't filter by user_id, leaking data across users

**Impact**: Critical security vulnerability, users see others' todos

**Mitigation**:
- Comprehensive user isolation tests
- Code review focusing on WHERE clauses
- Always pass user_id to CRUD operations
- Never trust user_id from request body

**Likelihood**: Low | **Severity**: Critical

### Risk 4: CORS Configuration

**Description**: CORS not configured correctly, frontend can't call API

**Impact**: API calls fail with CORS errors

**Mitigation**:
- Configure CORS middleware with specific frontend origin
- Enable credentials for Authorization header
- Test with real frontend during integration

**Likelihood**: Medium | **Severity**: Medium

## Success Criteria Mapping

| Success Criterion | Implementation Approach | Validation Method |
|-------------------|------------------------|-------------------|
| SC-001: All 5 endpoints functional | Implement routes in routers/todos.py | Integration tests for each endpoint |
| SC-002: 100% JWT verification | JWT dependency on all routes | Auth tests (missing, invalid, expired tokens) |
| SC-003: User isolation enforced | Filter queries by user_id | User isolation tests (403 for other users) |
| SC-004: Proper HTTP status codes | Exception handlers and route responses | Test all error scenarios |
| SC-005: 100 concurrent requests | Async operations with connection pooling | Load testing with pytest-asyncio |
| SC-006: Clear error messages | Consistent error format | Validation error tests |
| SC-007: User-scoped queries | WHERE user_id in all queries | Code review and isolation tests |
| SC-008: <200ms response time | Async operations, indexed queries | Performance testing with timing |

## Dependencies

### External Services
- **Better Auth** (Frontend): Issues JWT tokens with user identity
- **Neon PostgreSQL**: Serverless PostgreSQL database for data persistence
- **Frontend Application**: Consumes this API

### Python Libraries
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sqlmodel**: ORM with Pydantic integration
- **asyncpg**: Async PostgreSQL driver
- **python-jose**: JWT verification
- **pydantic-settings**: Environment configuration
- **pytest**: Testing framework
- **httpx**: HTTP client for testing

## Next Steps

1. **Review this plan** and approve architecture decisions
2. **Run `/sp.tasks`** to generate detailed implementation tasks
3. **Run `/sp.implement`** to execute tasks and build the backend
4. **Integration testing** with frontend application
5. **Create ADR** for significant decisions (JWT verification, async database)

## Notes

- All code examples and patterns are documented in `research.md`
- OpenAPI specification provides complete API contract
- Data model defines exact database schema
- Quickstart guide enables rapid setup for reviewers
- Constitution compliance verified at all gates
