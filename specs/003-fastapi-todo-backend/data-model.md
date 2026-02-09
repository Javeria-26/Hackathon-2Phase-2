# Data Model: FastAPI Todo Backend

**Feature**: 003-fastapi-todo-backend
**Date**: 2026-02-09
**Status**: Design Complete

---

## Overview

This document defines the database schema and data entities for the FastAPI Todo Backend. The system uses a single table design with user-scoped data isolation enforced at the query level.

---

## Database Schema

### Todo Table

**Table Name**: `todos`

**Purpose**: Store user-scoped todo items with title, description, completion status, and timestamps.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(36) | PRIMARY KEY | UUID v4 identifier for the todo |
| `user_id` | VARCHAR(255) | NOT NULL, INDEX | User identifier from JWT token |
| `title` | VARCHAR(200) | NOT NULL | Todo title (1-200 characters) |
| `description` | TEXT | DEFAULT '' | Optional todo description (0-1000 characters) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Indexes**:
- Primary key on `id` (automatic)
- Index on `user_id` for fast user-scoped queries
- Composite index on `(user_id, completed)` for filtered queries (optional optimization)

**SQL Schema** (PostgreSQL):
```sql
CREATE TABLE todos (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_completed ON todos(user_id, completed);
```

---

## Entity Definitions

### Todo Entity

**Description**: Represents a single todo item belonging to a user.

**Attributes**:

- **id** (string, UUID):
  - Unique identifier for the todo
  - Generated automatically using UUID v4
  - Immutable after creation
  - Example: `"550e8400-e29b-41d4-a716-446655440000"`

- **user_id** (string):
  - Identifier of the user who owns this todo
  - Extracted from JWT token claims (`sub` or `userId`)
  - Immutable after creation (todos cannot be transferred)
  - Used for data isolation (all queries filter by this field)
  - Example: `"user-123-abc"`

- **title** (string):
  - Short description of the todo
  - Required field (cannot be empty or whitespace-only)
  - Length: 1-200 characters
  - Trimmed of leading/trailing whitespace
  - Example: `"Buy groceries"`

- **description** (string):
  - Detailed description or notes for the todo
  - Optional field (defaults to empty string)
  - Length: 0-1000 characters
  - Trimmed of leading/trailing whitespace
  - Example: `"Milk, eggs, bread, and vegetables"`

- **completed** (boolean):
  - Indicates whether the todo is completed
  - Defaults to `false` for new todos
  - Can be toggled by user
  - Example: `false`

- **created_at** (datetime):
  - Timestamp when the todo was created
  - Set automatically on creation
  - Immutable after creation
  - Stored in UTC
  - Example: `"2026-02-09T10:30:00Z"`

- **updated_at** (datetime):
  - Timestamp when the todo was last modified
  - Set automatically on creation
  - Updated automatically on any modification
  - Stored in UTC
  - Example: `"2026-02-09T15:45:00Z"`

**Relationships**:
- Each todo belongs to exactly one user (identified by `user_id`)
- User entity is managed by Better Auth (not stored in this database)
- No foreign key constraint (user table doesn't exist in this service)

**Validation Rules**:
1. `title` must not be empty or whitespace-only
2. `title` length must be between 1 and 200 characters
3. `description` length must not exceed 1000 characters
4. `user_id` must be present and non-empty
5. `completed` must be a boolean value
6. `id` must be a valid UUID v4 string

---

## SQLModel Implementation

### Base Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TodoBase(SQLModel):
    """Base model with shared fields for Todo"""
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
```

### Database Model

```python
class Todo(TodoBase, table=True):
    """Database model for Todo table"""
    __tablename__ = "todos"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Request/Response Schemas

```python
class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass

class TodoUpdate(SQLModel):
    """Schema for updating a todo (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Schema for todo response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## Data Access Patterns

### Query Patterns

All database queries MUST filter by `user_id` to enforce data isolation:

**List all todos for a user**:
```sql
SELECT * FROM todos
WHERE user_id = ?
ORDER BY created_at DESC;
```

**List completed todos for a user**:
```sql
SELECT * FROM todos
WHERE user_id = ? AND completed = true
ORDER BY created_at DESC;
```

**Search todos by title/description**:
```sql
SELECT * FROM todos
WHERE user_id = ?
  AND (title ILIKE ? OR description ILIKE ?)
ORDER BY created_at DESC;
```

**Get specific todo (with user check)**:
```sql
SELECT * FROM todos
WHERE id = ? AND user_id = ?;
```

**Update todo (with user check)**:
```sql
UPDATE todos
SET title = ?, description = ?, completed = ?, updated_at = NOW()
WHERE id = ? AND user_id = ?;
```

**Delete todo (with user check)**:
```sql
DELETE FROM todos
WHERE id = ? AND user_id = ?;
```

### Security Considerations

1. **User Isolation**: Every query MUST include `WHERE user_id = ?` clause
2. **No Trust of Client Data**: Never use `user_id` from request body; always use authenticated user from JWT
3. **Authorization Check**: For single-item operations (get, update, delete), verify the todo belongs to the authenticated user
4. **Return 403 vs 404**: If a todo exists but belongs to another user, return 404 (not 403) to avoid information leakage

---

## Data Lifecycle

### Creation Flow

1. User sends POST request with `title` and optional `description`
2. Backend extracts `user_id` from JWT token
3. Backend validates input (title not empty, lengths within limits)
4. Backend generates UUID for `id`
5. Backend sets `created_at` and `updated_at` to current UTC time
6. Backend sets `completed` to `false`
7. Backend inserts record into database
8. Backend returns created todo with all fields

### Update Flow

1. User sends PUT request with updated fields
2. Backend extracts `user_id` from JWT token
3. Backend queries todo by `id` and `user_id`
4. If not found, return 404
5. Backend validates input
6. Backend updates specified fields
7. Backend sets `updated_at` to current UTC time
8. Backend commits changes
9. Backend returns updated todo

### Deletion Flow

1. User sends DELETE request with todo `id`
2. Backend extracts `user_id` from JWT token
3. Backend queries todo by `id` and `user_id`
4. If not found, return 404
5. Backend deletes record
6. Backend returns 204 No Content

---

## Performance Considerations

### Indexes

- **Primary Key Index** on `id`: Fast lookups by ID
- **Index on `user_id`**: Fast filtering by user (most common query pattern)
- **Composite Index on `(user_id, completed)`**: Optimizes filtered queries (optional)

### Query Optimization

- Use `ORDER BY created_at DESC` for consistent ordering
- Limit result sets if pagination is added later
- Use connection pooling to reduce connection overhead
- Use async queries to avoid blocking

### Scalability

- Single table design scales well for millions of todos
- User-scoped queries naturally partition data
- No complex joins or relationships
- Suitable for horizontal scaling with read replicas

---

## Migration Strategy

### Initial Schema Creation

SQLModel will automatically create the table on first run using:

```python
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Future Migrations

If schema changes are needed:
1. Use Alembic for migration management
2. Create migration scripts for schema changes
3. Test migrations on staging environment
4. Apply migrations with rollback plan

---

## Testing Data

### Test Fixtures

```python
# Test user IDs
TEST_USER_1 = "test-user-123"
TEST_USER_2 = "test-user-456"

# Sample todos
SAMPLE_TODO_1 = {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False
}

SAMPLE_TODO_2 = {
    "title": "Finish project",
    "description": "Complete FastAPI backend",
    "completed": True
}
```

### Test Scenarios

1. **User Isolation**: Create todos for User 1, verify User 2 cannot access them
2. **Filtering**: Create completed and incomplete todos, verify filters work
3. **Search**: Create todos with different titles, verify search works
4. **Validation**: Test empty title, too-long title, too-long description
5. **Timestamps**: Verify created_at and updated_at are set correctly

---

## Summary

- **Single table design** with user-scoped data isolation
- **7 columns**: id, user_id, title, description, completed, created_at, updated_at
- **Indexes** on user_id for fast queries
- **Validation** enforced at model level
- **Security** through user_id filtering on all queries
- **Performance** optimized for user-scoped access patterns
