# Phase II Multi-User Todo Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development must follow the spec-driven workflow:
1. Write specification (spec.md) defining requirements, boundaries, and contracts
2. Generate architectural plan (plan.md) with decisions and rationale
3. Break down into testable tasks (tasks.md) with acceptance criteria
4. Implement tasks incrementally with validation

**Requirements:**
- No implementation without approved specification
- Each feature must have clear boundaries and interfaces
- Specs must be independently reviewable and validatable
- All changes must reference originating spec/task

### II. Zero Manual Coding
All code generation must be performed via Claude Code using the Agentic Dev Stack workflow.

**Requirements:**
- No direct manual code editing outside the agentic workflow
- All implementations must be traceable to tasks
- Code must be generated with full context from specs and plans
- Manual interventions must be documented in PHRs

### III. Security-First Design (NON-NEGOTIABLE)
Security is a foundational requirement, not an afterthought.

**Authentication Requirements:**
- All API endpoints MUST require authentication
- Better Auth handles user authentication on frontend
- JWT tokens issued upon successful login
- JWT tokens passed via `Authorization: Bearer <token>` header
- FastAPI backend MUST verify JWT signatures using shared secret
- Backend MUST extract authenticated user identity from JWT claims

**Authorization Requirements:**
- Backend MUST validate authenticated user matches `user_id` in request path
- Users MUST NEVER access or modify other users' data
- Database queries MUST always filter by authenticated user ID
- Unauthorized requests MUST be rejected with appropriate HTTP status codes

**Data Isolation:**
- Each task belongs to exactly one authenticated user
- No cross-user data leakage permitted
- User data boundaries enforced at database, API, and UI layers

### IV. Clear Separation of Concerns
The system is divided into four independent specifications with well-defined boundaries:

1. **Frontend Spec (Next.js)**
   - User interface and authentication state management
   - JWT token handling and API communication
   - Protected route enforcement
   - User feedback and error handling

2. **Backend Spec (FastAPI)**
   - Stateless API service
   - JWT verification and user extraction
   - Business logic execution
   - Request validation and authorization

3. **Database Spec (Neon + SQLModel)**
   - Schema design and migrations
   - Data persistence and integrity
   - Serverless-safe connection patterns
   - User-scoped data access

4. **Authentication Spec (Better Auth)**
   - User registration and login
   - JWT token generation and management
   - Session handling
   - Authentication state

**Interface Requirements:**
- Specs communicate ONLY through documented interfaces
- No spec may assume internal details of another spec
- API contracts must be explicitly defined
- Breaking changes require cross-spec coordination

### V. Production-Ready Architecture
All implementations must meet production standards from the start.

**Quality Requirements:**
- Proper error handling with clear user feedback
- Graceful degradation for failure scenarios
- Scalable database patterns
- Secure credential management (no hardcoded secrets)
- Comprehensive input validation
- Appropriate HTTP status codes

**Operational Requirements:**
- Environment-based configuration via `.env`
- Serverless-compatible patterns
- Stateless backend design
- Connection pooling for database access

### VI. Minimal Viable Changes
Implement only what is specified; avoid scope creep and speculative features.

**Requirements:**
- No "nice-to-have" features outside stated requirements
- No refactoring of unrelated code
- Smallest viable diff for each change
- Clear justification for any additions

## Technology Standards

### Frontend Stack
- **Framework**: Next.js 16+ using App Router
- **Authentication**: Better Auth
- **API Communication**: Fetch API with JWT Bearer tokens
- **UI Requirements**: Responsive, user-friendly interface

### Backend Stack
- **Framework**: Python FastAPI
- **ORM**: SQLModel
- **Authentication**: JWT verification with shared secret
- **Architecture**: Stateless API service

### Database Stack
- **Provider**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Patterns**: Serverless-safe connections, user-scoped queries
- **Integrity**: Foreign keys, constraints, proper indexing

### Development Stack
- **Workflow Tool**: Claude Code
- **Methodology**: Spec-Kit Plus
- **Version Control**: Git with feature branches
- **Documentation**: PHRs and ADRs

## API Contract Standards

### Endpoint Structure
All API endpoints MUST conform to the following routes:

```
GET    /api/{user_id}/tasks           # List all tasks for user
POST   /api/{user_id}/tasks           # Create new task for user
GET    /api/{user_id}/tasks/{id}      # Get specific task
PUT    /api/{user_id}/tasks/{id}      # Update specific task
DELETE /api/{user_id}/tasks/{id}      # Delete specific task
PATCH  /api/{user_id}/tasks/{id}/complete  # Mark task complete
```

### Request Requirements
- All requests MUST include `Authorization: Bearer <jwt_token>` header
- Request body MUST be valid JSON for POST/PUT/PATCH
- Path parameters MUST be validated
- Query parameters MUST be sanitized

### Response Requirements
- All responses MUST be JSON-serializable
- Proper HTTP status codes MUST be used:
  - 200: Success
  - 201: Created
  - 204: No Content (for DELETE)
  - 400: Bad Request
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
  - 500: Internal Server Error
- Error responses MUST include descriptive messages
- Success responses MUST include relevant data

### Authentication Flow
1. User authenticates via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend includes JWT in all API requests
4. Backend verifies JWT signature
5. Backend extracts user identity from JWT claims
6. Backend validates user_id in path matches authenticated user
7. Backend executes authorized operation

## Data Standards

### Schema Requirements
- Each task MUST have a `user_id` foreign key
- User data MUST be isolated by `user_id`
- Proper indexes on frequently queried fields
- Timestamps for created/updated tracking
- Soft deletes where appropriate

### Query Requirements
- All queries MUST filter by authenticated user ID
- No raw SQL without parameterization
- Use ORM (SQLModel) for type safety
- Connection pooling for serverless environments

### Migration Requirements
- Schema changes via migration scripts
- Backward compatibility considerations
- Rollback procedures documented

## Development Workflow

### Spec Creation
1. Define feature requirements in natural language
2. Run `/sp.specify` to generate spec.md
3. Review and refine specification
4. Get user approval before proceeding

### Planning
1. Run `/sp.plan` to generate plan.md from spec
2. Document architectural decisions
3. Identify ADR-worthy decisions
4. Get user approval before task generation

### Task Generation
1. Run `/sp.tasks` to generate tasks.md from plan
2. Ensure tasks are testable and atomic
3. Define clear acceptance criteria
4. Order tasks by dependencies

### Implementation
1. Run `/sp.implement` to execute tasks
2. Validate each task completion
3. Run tests and verify functionality
4. Create PHR for significant work

### Documentation
- **PHRs**: Created for all user interactions and implementation work
- **ADRs**: Created for architecturally significant decisions
- **Code Comments**: Only where logic isn't self-evident

## Constraints

### Technology Constraints
- ONLY use approved frameworks and libraries listed in Technology Standards
- NO additional dependencies without explicit approval
- NO deviation from specified architecture patterns

### Scope Constraints
- NO features outside stated requirements
- NO speculative "future-proofing"
- NO refactoring unrelated to current task

### Security Constraints
- NO hardcoded secrets or credentials
- NO client-side trust of user identity
- NO cross-user data access
- NO unauthenticated endpoints

## Success Criteria

### Functional Requirements
✓ Users can sign up and sign in
✓ Users can create, read, update, delete their own tasks
✓ Users can mark tasks as complete
✓ Tasks persist across sessions and reloads
✓ Users cannot access other users' tasks

### Security Requirements
✓ All API endpoints require authentication
✓ JWT tokens properly verified on backend
✓ User identity validated on every request
✓ Data isolation enforced at all layers

### Quality Requirements
✓ Proper error handling with user feedback
✓ Responsive UI across devices
✓ Graceful handling of edge cases
✓ Production-ready code quality

### Documentation Requirements
✓ All four specs completed and approved
✓ PHRs created for implementation work
✓ ADRs created for significant decisions
✓ Clear API documentation

## Governance

### Constitution Authority
This constitution supersedes all other practices and guidelines. Any deviation requires:
1. Documented justification
2. User approval
3. Constitution amendment if pattern should be repeated

### Compliance Verification
- All PRs must verify compliance with constitution
- Spec reviews must check adherence to principles
- Implementation reviews must validate security requirements
- No shortcuts permitted for "quick fixes"

### Amendment Process
1. Identify need for constitutional change
2. Document rationale and impact
3. Update constitution with version increment
4. Communicate changes to all stakeholders
5. Update dependent templates and documentation

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
