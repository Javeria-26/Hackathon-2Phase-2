# Data Model: Todo Task Schema

**Feature**: 001-neon-postgres-todos
**Date**: 2026-02-09
**Database**: Neon Serverless PostgreSQL

## Overview

This document defines the database schema for user-scoped todo tasks. The schema enforces strict user isolation through foreign key constraints and indexed queries.

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │ (Managed by Auth System - Phase I)
├─────────────────┤
│ id (PK)         │
│ email           │
│ ...             │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────┐
│     todos       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │◄── Indexed for fast filtering
│ title           │
│ description     │
│ completed       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Table: todos

### Schema Definition

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| user_id | VARCHAR(255) | NOT NULL, INDEXED, FOREIGN KEY | Owner of the task |
| title | VARCHAR(500) | NOT NULL | Task title (1-500 characters) |
| description | VARCHAR(5000) | DEFAULT '' | Task description (0-5000 characters) |
| completed | BOOLEAN | NOT NULL, DEFAULT false | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

### Indexes

1. **Primary Index**: `todos_pkey` on `id`
   - Type: B-tree
   - Purpose: Unique identification and fast lookups by ID

2. **User Filter Index**: `ix_todos_user_id` on `user_id`
   - Type: B-tree
   - Purpose: Fast filtering of tasks by user

3. **Composite Index**: `ix_todos_user_created` on `(user_id, created_at DESC)`
   - Type: B-tree
   - Purpose: Optimized for common query pattern (user's tasks ordered by creation date)
   - Query: `SELECT * FROM todos WHERE user_id = ? ORDER BY created_at DESC`

### Constraints

1. **Primary Key**: `id` must be unique and not null
2. **Foreign Key**: `user_id` references `users.id` (managed by auth system)
3. **Not Null**: `user_id`, `title`, `completed`, `created_at`, `updated_at`
4. **Check Constraints**:
   - `title` length: 1-500 characters (enforced at application level)
   - `description` length: 0-5000 characters (enforced at application level)
5. **Default Values**:
   - `completed`: false
   - `created_at`: CURRENT_TIMESTAMP
   - `updated_at`: CURRENT_TIMESTAMP

## SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Todo(SQLModel, table=True):
    """Database model for user-scoped todo tasks."""
    __tablename__ = "todos"

    # Primary key
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )

    # Foreign key to users table
    user_id: str = Field(
        index=True,
        nullable=False
    )

    # Task content
    title: str = Field(
        min_length=1,
        max_length=500,
        nullable=False
    )

    description: str = Field(
        default="",
        max_length=5000
    )

    # Status
    completed: bool = Field(
        default=False,
        nullable=False
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

## SQL Schema (PostgreSQL)

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(5000) DEFAULT '',
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for user filtering
CREATE INDEX ix_todos_user_id ON todos(user_id);

-- Composite index for user + ordering
CREATE INDEX ix_todos_user_created ON todos(user_id, created_at DESC);

-- Foreign key constraint (if users table exists)
ALTER TABLE todos
ADD CONSTRAINT fk_todos_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
```

## Data Types Rationale

### UUID for Primary Key
- **Security**: Prevents ID enumeration attacks
- **Distribution**: Globally unique, no coordination needed
- **Concurrency**: No collision risk with simultaneous inserts
- **Trade-off**: Larger storage (16 bytes) vs integer (4-8 bytes)

### VARCHAR for user_id
- **Flexibility**: Supports various auth system ID formats (UUID, string, etc.)
- **Compatibility**: Works with Better Auth user IDs
- **Length**: 255 characters sufficient for any reasonable ID format

### VARCHAR for title/description
- **Length Limits**: Prevents abuse and ensures reasonable data sizes
- **Title**: 500 characters (typical sentence length)
- **Description**: 5000 characters (multiple paragraphs)

### BOOLEAN for completed
- **Native Type**: PostgreSQL has native boolean support
- **Clarity**: More explicit than integer flags (0/1)
- **Performance**: Efficient storage (1 byte)

### TIMESTAMP for dates
- **Precision**: Microsecond precision for accurate ordering
- **UTC**: All timestamps stored in UTC to avoid timezone issues
- **Auto-update**: updated_at should be updated on every modification

## Query Patterns

### Common Queries

1. **Get all tasks for a user (ordered by creation date)**
   ```sql
   SELECT * FROM todos
   WHERE user_id = $1
   ORDER BY created_at DESC
   LIMIT $2 OFFSET $3;
   ```
   - Uses: `ix_todos_user_created` composite index
   - Performance: O(log n) + result set size

2. **Get specific task for a user**
   ```sql
   SELECT * FROM todos
   WHERE id = $1 AND user_id = $2;
   ```
   - Uses: `todos_pkey` primary index + user_id filter
   - Performance: O(log n)

3. **Update task (with ownership check)**
   ```sql
   UPDATE todos
   SET title = $1, description = $2, completed = $3, updated_at = NOW()
   WHERE id = $4 AND user_id = $5
   RETURNING *;
   ```
   - Uses: `todos_pkey` primary index + user_id filter
   - Performance: O(log n)

4. **Delete task (with ownership check)**
   ```sql
   DELETE FROM todos
   WHERE id = $1 AND user_id = $2;
   ```
   - Uses: `todos_pkey` primary index + user_id filter
   - Performance: O(log n)

5. **Count tasks for a user**
   ```sql
   SELECT COUNT(*) FROM todos
   WHERE user_id = $1;
   ```
   - Uses: `ix_todos_user_id` index
   - Performance: O(n) where n = user's task count

## Performance Considerations

### Index Selection
- **Composite index covers single-column**: `(user_id, created_at)` can be used for queries filtering only by `user_id`
- **Index size**: Composite index is larger but eliminates need for separate sort
- **Write overhead**: Each insert/update maintains all indexes (acceptable for todo app)

### Query Optimization
- **Pagination**: Use LIMIT/OFFSET to avoid loading all tasks
- **Selective columns**: Use SELECT specific columns when full row not needed
- **Connection pooling**: Reuse connections to avoid connection overhead

### Scalability
- **Per-user partitioning**: Not needed for expected scale (<1000 tasks per user)
- **Archival**: Out of scope (no soft deletes or archival in this phase)
- **Sharding**: Not needed for single-database deployment

## Data Integrity

### Referential Integrity
- **Foreign Key**: `user_id` references `users.id`
- **Cascade Delete**: When user deleted, all their tasks deleted (ON DELETE CASCADE)
- **Orphan Prevention**: Cannot create task without valid user_id

### Validation Rules
1. **Title**: Must not be empty or whitespace-only
2. **Description**: Can be empty, but if provided must be ≤5000 characters
3. **User ID**: Must be valid user from auth system
4. **Timestamps**: Auto-managed, cannot be manually set to future dates

### Concurrency Control
- **Isolation Level**: READ COMMITTED (PostgreSQL default)
- **Locking**: No explicit locks needed for todo operations
- **Conflicts**: Last write wins (acceptable for todo app)

## Migration Notes

### From SQLite to PostgreSQL
- **Type Changes**: SQLite TEXT → PostgreSQL VARCHAR/UUID/TIMESTAMP
- **Boolean**: SQLite INTEGER (0/1) → PostgreSQL BOOLEAN
- **UUID**: SQLite TEXT → PostgreSQL UUID (native type)
- **Indexes**: Recreate with PostgreSQL-specific syntax

### Schema Evolution
- **Adding Columns**: Use ALTER TABLE ADD COLUMN with DEFAULT
- **Removing Columns**: Use ALTER TABLE DROP COLUMN (check dependencies first)
- **Changing Types**: Requires data migration (e.g., TEXT to UUID)

## Testing Considerations

### Test Data
```python
# Valid test todo
test_todo = {
    "user_id": "test-user-123",
    "title": "Test Task",
    "description": "Test description",
    "completed": False
}

# Edge cases
edge_cases = [
    {"title": "A" * 500},           # Max length title
    {"description": "B" * 5000},    # Max length description
    {"title": "   Trimmed   "},     # Whitespace handling
    {"description": ""},            # Empty description
]
```

### Isolation Tests
```python
# Create tasks for two users
user_a_task = create_todo(session, "user-a", {...})
user_b_task = create_todo(session, "user-b", {...})

# Verify user A cannot access user B's task
result = get_todo(session, "user-a", user_b_task.id)
assert result is None  # Should not find task
```

## Summary

- **Table**: `todos` with 7 columns
- **Indexes**: 3 (primary, user_id, composite)
- **Constraints**: Foreign key, NOT NULL, defaults
- **Performance**: <100ms queries for 1000 tasks per user
- **Security**: User isolation enforced at database level
