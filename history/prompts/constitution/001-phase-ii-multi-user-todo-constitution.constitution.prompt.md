---
id: 001
title: Phase II Multi-User Todo Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "security", "spec-driven-development", "architecture", "multi-user", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Phase II – Multi-User Todo Full-Stack Web Application

Objective:

Transform an existing console-based Todo application into a modern, multi-user, full-stack web application with persistent storage, authentication, and secured REST APIs using a fully spec-driven, agentic development workflow.

Core principles:

- Spec-driven development (write spec → generate plan → break into tasks → implement)
- Zero manual coding (all code generated via Claude Code)
- Clear separation of concerns across system layers
- Security-first design with strict user data isolation
- Production-ready architecture and practices

Technology standards:

- Frontend: Next.js 16+ using App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (Next.js)
- Authorization: JWT Bearer Tokens
- Development workflow: Claude Code + Spec-Kit Plus

API standards:

- RESTful API design
- All endpoints must conform exactly to the following routes:
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete
- Proper HTTP status codes must be used for all responses
- API responses must be JSON-serializable

Authentication & security principles:

- All API endpoints must require authentication
- Authentication must be implemented using Better Auth on the frontend
- Better Auth must issue JWT tokens upon successful login
- JWT tokens must be passed via the Authorization: Bearer <token> header
- FastAPI backend must verify JWT signatures using a shared secret
- Backend must extract authenticated user identity from JWT claims
- Backend must validate that the authenticated user matches the user_id in the request path
- Users must never be able to access or modify other users' data

Data & persistence standards:

- All data must be persisted in Neon Serverless PostgreSQL
- Each task must belong to exactly one authenticated user
- Database queries must always be filtered by authenticated user ID
- Schema design must support scalability and data integrity
- Serverless-safe database connection patterns must be used

Frontend standards:

- Responsive, user-friendly interface
- Authentication state must be enforced across protected routes
- JWT tokens must be attached to every backend API request
- UI must support all basic Todo functionality (create, read, update, delete, complete)
- Errors must be handled gracefully with clear user feedback

Backend standards:

- FastAPI must act as a stateless API service
- JWT verification must occur on every request
- Business logic must be clearly separated from infrastructure concerns
- Unauthorized or invalid requests must be rejected securely
- Backend must never trust client-supplied user identifiers without verification

Spec boundaries:

- The system must be divided into four independent specs:
  1. Frontend (Next.js)
  2. FastAPI Backend
  3. Database (Neon + SQLModel)
  4. Authentication (Better Auth)
- Each spec must define responsibilities, inputs, outputs, constraints, and failure cases
- Specs must communicate only through well-defined interfaces (API contracts, JWT claims, schema)
- No spec may assume internal details of another spec beyond documented interfaces

Constraints:

- No additional frameworks, libraries, or services beyond those explicitly approved
- No speculative or "nice-to-have" features outside the stated requirements
- No deviation from the Agentic Dev Stack workflow

Success criteria:

- Users can sign up, sign in, and manage only their own tasks
- Tasks persist across sessions and reloads
- REST APIs are fully secured and user-scoped
- Application is functionally complete, secure, and production-ready
- Each spec can be reviewed, implemented, and validated independently

## Response snapshot

Created comprehensive project constitution at `.specify/memory/constitution.md` with the following structure:

**Core Principles (6 NON-NEGOTIABLE principles):**
1. Spec-Driven Development - mandatory workflow: spec → plan → tasks → implement
2. Zero Manual Coding - all code via Claude Code agentic workflow
3. Security-First Design - authentication, authorization, and data isolation requirements
4. Clear Separation of Concerns - four independent specs with defined boundaries
5. Production-Ready Architecture - quality and operational requirements
6. Minimal Viable Changes - no scope creep or speculative features

**Technology Standards:**
- Frontend: Next.js 16+ with Better Auth
- Backend: Python FastAPI with JWT verification
- Database: Neon Serverless PostgreSQL with SQLModel
- Development: Claude Code + Spec-Kit Plus

**API Contract Standards:**
- Defined exact endpoint structure for all 6 routes
- Request/response requirements with proper HTTP status codes
- Complete authentication flow documentation

**Data Standards:**
- Schema requirements with user_id foreign keys
- Query requirements with user filtering
- Migration requirements

**Development Workflow:**
- Spec creation, planning, task generation, implementation steps
- PHR and ADR documentation requirements

**Constraints & Success Criteria:**
- Technology, scope, and security constraints clearly defined
- Functional, security, quality, and documentation success criteria

**Governance:**
- Constitution authority and compliance verification
- Amendment process documented

Version 1.0.0 ratified on 2026-02-08.

## Outcome

- ✅ Impact: Established foundational project constitution defining all development principles, security requirements, technology standards, and workflows for Phase II multi-user todo application
- 🧪 Tests: N/A - constitution is a governance document
- 📁 Files: Created .specify/memory/constitution.md (295 lines)
- 🔁 Next prompts: Create four independent specs (Frontend, Backend, Database, Authentication) following the spec-driven workflow
- 🧠 Reflection: Constitution successfully captures all security-first requirements, clear separation of concerns, and production-ready standards. Ready to proceed with spec creation for each system component.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - constitution creation
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.specify for first feature spec (likely authentication or database as foundation)
