# Feature Specification: FastAPI Todo Backend

**Feature Branch**: `003-fastapi-todo-backend`
**Created**: 2026-02-09
**Status**: Draft
**Input**: User description: "Phase II – FastAPI Backend (Todo API) - Implement a secure FastAPI service that exposes user-scoped Todo REST APIs and verifies JWTs issued by Better Auth."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Manage Personal Todos (Priority: P1)

As an authenticated user, I want to create, view, update, and delete my personal todo items so that I can track my tasks independently from other users.

**Why this priority**: This is the core functionality of the todo system. Without CRUD operations on todos, the application has no value. This represents the minimum viable product.

**Independent Test**: Can be fully tested by authenticating a user, creating a todo item, verifying it appears in their list, updating it, and deleting it. Delivers immediate value as a functional personal task manager.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user, **When** I send a POST request to create a new todo with title and description, **Then** the system creates the todo, assigns it to my user ID, and returns the created todo with a unique ID and timestamps
2. **Given** I am an authenticated user with existing todos, **When** I send a GET request to list my todos, **Then** the system returns only my todos (not other users' todos)
3. **Given** I am an authenticated user with an existing todo, **When** I send a PUT request to update the todo's title, description, or completion status, **Then** the system updates only that todo and returns the updated version
4. **Given** I am an authenticated user with an existing todo, **When** I send a DELETE request for that todo, **Then** the system removes the todo and returns a success confirmation
5. **Given** I am an authenticated user, **When** I attempt to update or delete another user's todo, **Then** the system returns a 403 Forbidden error

---

### User Story 2 - Secure API Access with JWT Authentication (Priority: P1)

As a system administrator, I want all API endpoints to verify JWT tokens issued by Better Auth so that only authenticated users can access the todo API and users can only access their own data.

**Why this priority**: Security is non-negotiable for a multi-user system. Without proper authentication, the API would be vulnerable to unauthorized access and data breaches. This must be implemented from the start.

**Independent Test**: Can be tested by attempting to access endpoints without a token (should fail with 401), with an invalid token (should fail with 401), and with a valid token (should succeed). Verifies the security boundary is properly enforced.

**Acceptance Scenarios**:

1. **Given** I send a request without an Authorization header, **When** the request reaches any protected endpoint, **Then** the system returns a 401 Unauthorized error with a clear message
2. **Given** I send a request with an invalid or expired JWT token, **When** the request reaches any protected endpoint, **Then** the system returns a 401 Unauthorized error
3. **Given** I send a request with a valid JWT token, **When** the request reaches any protected endpoint, **Then** the system extracts the user ID from the token and processes the request
4. **Given** I am authenticated as User A, **When** I attempt to access User B's todo by ID, **Then** the system returns a 403 Forbidden error

---

### User Story 3 - Filter and Query Todos (Priority: P2)

As an authenticated user, I want to filter my todos by completion status and search by title so that I can quickly find specific tasks.

**Why this priority**: While not essential for MVP, filtering significantly improves usability for users with many todos. This is a common user need that enhances the core functionality.

**Independent Test**: Can be tested by creating multiple todos with different statuses, then querying with filters (e.g., ?completed=true) and verifying only matching todos are returned.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with both completed and incomplete todos, **When** I send a GET request with query parameter ?completed=false, **Then** the system returns only my incomplete todos
2. **Given** I am an authenticated user with multiple todos, **When** I send a GET request with query parameter ?search=meeting, **Then** the system returns only my todos whose title or description contains "meeting" (case-insensitive)
3. **Given** I am an authenticated user, **When** I send a GET request with multiple filters (?completed=true&search=work), **Then** the system returns todos matching all criteria

---

### User Story 4 - Retrieve Single Todo Details (Priority: P2)

As an authenticated user, I want to retrieve a specific todo by its ID so that I can view its complete details.

**Why this priority**: Useful for detailed views and direct access to specific todos, but the list endpoint can serve most needs initially.

**Independent Test**: Can be tested by creating a todo, noting its ID, then retrieving it by ID and verifying all fields match.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with an existing todo, **When** I send a GET request to /todos/{id} with my todo's ID, **Then** the system returns the complete todo details
2. **Given** I am an authenticated user, **When** I send a GET request to /todos/{id} with a non-existent ID, **Then** the system returns a 404 Not Found error
3. **Given** I am an authenticated user, **When** I send a GET request to /todos/{id} with another user's todo ID, **Then** the system returns a 403 Forbidden error

---

### Edge Cases

- What happens when a user sends malformed JSON in the request body? (System should return 422 Unprocessable Entity with validation errors)
- What happens when a user tries to create a todo with an empty title? (System should return 422 with validation error requiring non-empty title)
- What happens when the JWT token expires mid-session? (System should return 401 and client should refresh token)
- What happens when the database connection fails? (System should return 503 Service Unavailable with appropriate error message)
- What happens when a user sends extremely long title or description (e.g., 10,000 characters)? (System should enforce reasonable length limits and return 422 if exceeded)
- What happens when concurrent requests try to update the same todo? (System should handle with database-level locking or last-write-wins strategy)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a REST API endpoint to create a new todo item with title (required), description (optional), and completed status (defaults to false)
- **FR-002**: System MUST provide a REST API endpoint to retrieve all todos belonging to the authenticated user
- **FR-003**: System MUST provide a REST API endpoint to retrieve a single todo by ID, returning 404 if not found or 403 if not owned by the authenticated user
- **FR-004**: System MUST provide a REST API endpoint to update an existing todo's title, description, or completed status
- **FR-005**: System MUST provide a REST API endpoint to delete a todo by ID
- **FR-006**: System MUST verify JWT tokens on every API request using the shared secret from Better Auth
- **FR-007**: System MUST extract the user ID from the verified JWT token and use it to scope all todo operations
- **FR-008**: System MUST prevent users from accessing, modifying, or deleting todos that belong to other users
- **FR-009**: System MUST return appropriate HTTP status codes: 200 for success, 201 for creation, 400 for bad requests, 401 for unauthorized, 403 for forbidden, 404 for not found, 422 for validation errors, 500 for server errors
- **FR-010**: System MUST validate all input data and return clear error messages for validation failures
- **FR-011**: System MUST persist all todo data to a PostgreSQL database using SQLModel ORM
- **FR-012**: System MUST support filtering todos by completion status via query parameters
- **FR-013**: System MUST support searching todos by title or description via query parameters
- **FR-014**: System MUST automatically set created_at and updated_at timestamps for all todos
- **FR-015**: System MUST handle database connection errors gracefully and return appropriate error responses

### Key Entities

- **Todo**: Represents a task item with the following attributes:
  - Unique identifier (ID)
  - Title (required, non-empty string)
  - Description (optional text)
  - Completion status (boolean, defaults to false)
  - Owner (user ID from JWT token)
  - Creation timestamp
  - Last update timestamp
  - Relationship: Each todo belongs to exactly one user

- **User**: Represents the authenticated user (managed by Better Auth, not stored in this service):
  - User ID (extracted from JWT token)
  - Used to scope all todo operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All five REST endpoints (create, list, get, update, delete) are implemented and return correct responses for valid requests
- **SC-002**: 100% of API requests without valid JWT tokens are rejected with 401 Unauthorized status
- **SC-003**: Users can only access their own todos - attempting to access another user's todo returns 403 Forbidden
- **SC-004**: API returns appropriate HTTP status codes for all scenarios (success, validation errors, not found, forbidden, server errors)
- **SC-005**: API handles at least 100 concurrent requests without errors or data corruption
- **SC-006**: All validation errors return clear, actionable error messages in a consistent JSON format
- **SC-007**: Database queries are scoped by user ID, preventing any cross-user data leakage
- **SC-008**: API response time for list and get operations is under 200ms for datasets up to 1000 todos per user

## Scope & Boundaries *(mandatory)*

### In Scope

- REST API endpoints for todo CRUD operations
- JWT token verification using shared secret from Better Auth
- User-scoped data access (users can only see/modify their own todos)
- Input validation and error handling
- PostgreSQL database integration using SQLModel
- Filtering and search functionality for todos
- Proper HTTP status codes and error responses

### Out of Scope

- User authentication and registration (handled by Better Auth in the frontend)
- Frontend UI or client applications
- Real-time updates or WebSocket connections
- File attachments or media uploads for todos
- Todo sharing or collaboration features
- Email notifications or reminders
- User profile management
- Rate limiting or API throttling (can be added later if needed)
- API versioning (v1 is implicit for initial release)

### Dependencies

- **Better Auth**: Frontend service that issues JWT tokens; this backend must use the same shared secret to verify tokens
- **Neon PostgreSQL**: Database service for persisting todo data
- **Frontend Application**: Will consume this API (already implemented in Phase I)

### Assumptions

- JWT tokens issued by Better Auth contain a user ID claim that can be extracted
- The shared secret for JWT verification is available via environment variable
- Database connection string is provided via environment variable
- Standard REST conventions are followed (GET for retrieval, POST for creation, PUT for updates, DELETE for deletion)
- JSON is the data format for all requests and responses
- CORS will be configured to allow requests from the frontend origin
- The database schema will be created automatically by SQLModel on first run
- Todos have a simple flat structure (no nested subtasks or categories in MVP)
- Pagination is not required initially (can be added if performance issues arise)
