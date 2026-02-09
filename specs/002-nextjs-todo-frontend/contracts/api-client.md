# API Client Contracts: Next.js Todo Frontend

**Date**: 2026-02-08
**Feature**: 002-nextjs-todo-frontend
**Purpose**: Define all API endpoint contracts for frontend-backend communication

---

## Overview

This document defines the complete API contract between the Next.js frontend and the FastAPI backend. All endpoints require JWT authentication via the `Authorization: Bearer <token>` header unless otherwise specified.

**Base URL**: Configured via `NEXT_PUBLIC_API_URL` environment variable

---

## Authentication Endpoints

### Register User

**Endpoint**: `POST /api/auth/register`

**Description**: Create a new user account

**Authentication**: None (public endpoint)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```typescript
{
  email: string      // Valid email address
  password: string   // Min 8 chars, complexity requirements
}
```

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (201 Created):
```typescript
{
  user: {
    id: string
    email: string
  }
  token: string      // JWT token (24-hour expiration)
}
```

**Success Example**:
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

400 Bad Request - Invalid input:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": "Invalid email format",
      "password": "Password must be at least 8 characters"
    }
  }
}
```

409 Conflict - Email already exists:
```json
{
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email address is already registered"
  }
}
```

---

### Login User

**Endpoint**: `POST /api/auth/login`

**Description**: Authenticate existing user

**Authentication**: None (public endpoint)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```typescript
{
  email: string
  password: string
}
```

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (200 OK):
```typescript
{
  user: {
    id: string
    email: string
  }
  token: string      // JWT token (24-hour expiration)
}
```

**Success Example**:
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

400 Bad Request - Invalid input:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data"
  }
}
```

401 Unauthorized - Invalid credentials:
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

**Security Note**: Error message does not reveal whether email exists to prevent user enumeration.

---

### Logout User

**Endpoint**: `POST /api/auth/logout`

**Description**: Terminate user session

**Authentication**: Required (JWT token)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```typescript
{
  success: boolean
}
```

**Success Example**:
```json
{
  "success": true
}
```

**Error Responses**:

401 Unauthorized - Invalid or expired token:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired authentication token"
  }
}
```

---

## Todo Endpoints

### Get All Todos

**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieve all todos for authenticated user

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```typescript
{
  tasks: Array<{
    id: string
    title: string
    description: string
    completed: boolean
    userId: string
    createdAt: string      // ISO 8601 format
    updatedAt: string      // ISO 8601 format
  }>
}
```

**Success Example**:
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Complete project documentation",
      "description": "Write comprehensive docs for the frontend",
      "completed": false,
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "createdAt": "2026-02-08T10:30:00Z",
      "updatedAt": "2026-02-08T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Review pull requests",
      "description": "",
      "completed": true,
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "createdAt": "2026-02-07T14:20:00Z",
      "updatedAt": "2026-02-08T09:15:00Z"
    }
  ]
}
```

**Empty List Response**:
```json
{
  "tasks": []
}
```

**Error Responses**:

401 Unauthorized - Missing or invalid token:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden - User ID mismatch:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

---

### Create Todo

**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new todo for authenticated user

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```typescript
{
  title: string          // Required, 1-200 characters
  description: string    // Optional, 0-1000 characters
}
```

**Request Example**:
```json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication with Better Auth"
}
```

**Success Response** (201 Created):
```typescript
{
  task: {
    id: string
    title: string
    description: string
    completed: boolean     // Always false for new tasks
    userId: string
    createdAt: string
    updatedAt: string
  }
}
```

**Success Example**:
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "title": "Implement user authentication",
    "description": "Add JWT-based authentication with Better Auth",
    "completed": false,
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "createdAt": "2026-02-08T11:00:00Z",
    "updatedAt": "2026-02-08T11:00:00Z"
  }
}
```

**Error Responses**:

400 Bad Request - Invalid input:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "title": "Title is required and must be 1-200 characters",
      "description": "Description must be 0-1000 characters"
    }
  }
}
```

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

---

### Get Single Todo

**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieve a specific todo by ID

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)
- `id` (string): Todo ID

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```typescript
{
  task: {
    id: string
    title: string
    description: string
    completed: boolean
    userId: string
    createdAt: string
    updatedAt: string
  }
}
```

**Success Example**:
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the frontend",
    "completed": false,
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "createdAt": "2026-02-08T10:30:00Z",
    "updatedAt": "2026-02-08T10:30:00Z"
  }
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

404 Not Found:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Todo not found"
  }
}
```

---

### Update Todo

**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update an existing todo's title and description

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)
- `id` (string): Todo ID

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```typescript
{
  title: string          // Required, 1-200 characters
  description: string    // Optional, 0-1000 characters
}
```

**Request Example**:
```json
{
  "title": "Complete project documentation (updated)",
  "description": "Write comprehensive docs including API contracts"
}
```

**Success Response** (200 OK):
```typescript
{
  task: {
    id: string
    title: string
    description: string
    completed: boolean     // Unchanged
    userId: string
    createdAt: string      // Unchanged
    updatedAt: string      // Updated to current timestamp
  }
}
```

**Success Example**:
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete project documentation (updated)",
    "description": "Write comprehensive docs including API contracts",
    "completed": false,
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "createdAt": "2026-02-08T10:30:00Z",
    "updatedAt": "2026-02-08T11:30:00Z"
  }
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "title": "Title is required and must be 1-200 characters"
    }
  }
}
```

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

404 Not Found:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Todo not found"
  }
}
```

---

### Mark Todo Complete/Incomplete

**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle todo completion status

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)
- `id` (string): Todo ID

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```typescript
{
  completed: boolean     // true to mark complete, false to mark incomplete
}
```

**Request Example**:
```json
{
  "completed": true
}
```

**Success Response** (200 OK):
```typescript
{
  task: {
    id: string
    title: string
    description: string
    completed: boolean     // Updated value
    userId: string
    createdAt: string      // Unchanged
    updatedAt: string      // Updated to current timestamp
  }
}
```

**Success Example**:
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the frontend",
    "completed": true,
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "createdAt": "2026-02-08T10:30:00Z",
    "updatedAt": "2026-02-08T12:00:00Z"
  }
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "completed": "Must be a boolean value"
    }
  }
}
```

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

404 Not Found:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Todo not found"
  }
}
```

---

### Delete Todo

**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Permanently delete a todo

**Authentication**: Required (JWT token)

**Path Parameters**:
- `user_id` (string): User ID (must match authenticated user from JWT)
- `id` (string): Todo ID

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (204 No Content):
No response body

**Error Responses**:

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

403 Forbidden:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied: user_id does not match authenticated user"
  }
}
```

404 Not Found:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Todo not found"
  }
}
```

---

## Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input data, see details for field-level errors |
| UNAUTHORIZED | 401 | Missing, invalid, or expired authentication token |
| FORBIDDEN | 403 | User lacks permission to access resource |
| NOT_FOUND | 404 | Requested resource does not exist |
| EMAIL_EXISTS | 409 | Email address already registered |
| INVALID_CREDENTIALS | 401 | Incorrect email or password |
| SERVER_ERROR | 500 | Internal server error |

---

## JWT Token Structure

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "iat": 1707390000,
  "exp": 1707476400
}
```

**Expiration**: 24 hours from issuance

**Usage**: Include in Authorization header as `Bearer <token>`

---

## Rate Limiting

**Note**: Rate limiting is handled by the backend. Frontend should handle 429 Too Many Requests responses gracefully.

**Expected Limits** (backend-defined):
- Authentication endpoints: 5 requests per minute per IP
- Todo endpoints: 100 requests per minute per user

**429 Response**:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retryAfter": 60
  }
}
```

---

## CORS Configuration

**Expected CORS Headers** (from backend):
```
Access-Control-Allow-Origin: <frontend-origin>
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

---

## TypeScript Type Definitions

```typescript
// API Client Types
export interface ApiClient {
  get<T>(endpoint: string): Promise<T>
  post<T>(endpoint: string, data: any): Promise<T>
  put<T>(endpoint: string, data: any): Promise<T>
  patch<T>(endpoint: string, data: any): Promise<T>
  delete(endpoint: string): Promise<void>
}

// Authentication Types
export interface RegisterRequest {
  email: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface AuthResponse {
  user: {
    id: string
    email: string
  }
  token: string
}

// Todo Types
export interface CreateTodoRequest {
  title: string
  description: string
}

export interface UpdateTodoRequest {
  title: string
  description: string
}

export interface CompleteTodoRequest {
  completed: boolean
}

export interface TodoResponse {
  task: Todo
}

export interface TodoListResponse {
  tasks: Todo[]
}

// Error Types
export interface ApiError {
  error: {
    code: string
    message: string
    details?: Record<string, string>
  }
}
```

---

**Status**: API contracts complete, ready for quickstart guide
