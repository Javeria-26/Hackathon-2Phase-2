# CRUD Operations Contract

**Feature**: 001-neon-postgres-todos
**Date**: 2026-02-09
**Purpose**: Define database operation interfaces for user-scoped todo tasks

## Overview

This document defines the contract for all database CRUD (Create, Read, Update, Delete) operations on todo tasks. All operations enforce user-level data isolation by requiring a `user_id` parameter.

## Core Principle: User Isolation

**CRITICAL**: Every operation MUST filter by `user_id` to prevent cross-user data access. No operation should ever return or modify tasks belonging to a different user.

## Operation Signatures

### 1. Create Todo

**Function**: `create_todo(session: AsyncSession, user_id: str, todo_data: TodoCreate) -> Todo`

**Purpose**: Create a new todo task for a specific user.

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user creating the task (string)
- `todo_data`: Todo creation data (TodoCreate schema)
  - `title`: Task title (required, 1-500 chars)
  - `description`: Task description (optional, 0-5000 chars)
  - `completed`: Completion status (optional, default: false)

**Returns**: Created Todo object with all fields populated

**Behavior**:
- Generates unique UUID for `id`
- Sets `user_id` to provided value
- Sets `created_at` and `updated_at` to current UTC time
- Validates title is not empty or whitespace
- Trims whitespace from title and description

**Errors**:
- `ValueError`: If title is empty or exceeds length limits
- `DatabaseError`: If database operation fails

**Example**:
```python
todo_data = TodoCreate(
    title="Buy groceries",
    description="Milk, eggs, bread"
)
todo = await create_todo(session, "user-123", todo_data)
# Returns: Todo(id="uuid", user_id="user-123", title="Buy groceries", ...)
```

---

### 2. Get Todos (List)

**Function**: `get_todos(session: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Todo]`

**Purpose**: Retrieve all todo tasks for a specific user, ordered by creation date (newest first).

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user whose tasks to retrieve (string)
- `skip`: Number of records to skip for pagination (optional, default: 0)
- `limit`: Maximum number of records to return (optional, default: 100)

**Returns**: List of Todo objects (may be empty)

**Behavior**:
- Filters by `user_id` (MANDATORY)
- Orders by `created_at DESC` (newest first)
- Applies pagination (skip/limit)
- Returns empty list if user has no tasks

**Errors**:
- `DatabaseError`: If database operation fails

**Example**:
```python
# Get first 10 tasks for user
todos = await get_todos(session, "user-123", skip=0, limit=10)
# Returns: [Todo(...), Todo(...), ...]

# Get next 10 tasks (pagination)
todos = await get_todos(session, "user-123", skip=10, limit=10)
```

---

### 3. Get Todo (Single)

**Function**: `get_todo(session: AsyncSession, user_id: str, todo_id: str) -> Todo | None`

**Purpose**: Retrieve a specific todo task by ID, with user ownership validation.

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user requesting the task (string)
- `todo_id`: ID of the task to retrieve (UUID string)

**Returns**:
- Todo object if found and belongs to user
- `None` if not found or belongs to different user

**Behavior**:
- Filters by both `id` AND `user_id` (MANDATORY)
- Returns `None` if task doesn't exist
- Returns `None` if task exists but belongs to different user (prevents information leakage)

**Errors**:
- `DatabaseError`: If database operation fails

**Example**:
```python
# Get task that belongs to user
todo = await get_todo(session, "user-123", "task-uuid-456")
# Returns: Todo(...) if found and owned by user-123

# Try to get task belonging to different user
todo = await get_todo(session, "user-123", "other-user-task-uuid")
# Returns: None (prevents cross-user access)
```

---

### 4. Update Todo

**Function**: `update_todo(session: AsyncSession, user_id: str, todo_id: str, todo_data: TodoUpdate) -> Todo | None`

**Purpose**: Update a specific todo task with user ownership validation.

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user updating the task (string)
- `todo_id`: ID of the task to update (UUID string)
- `todo_data`: Update data (TodoUpdate schema)
  - `title`: New title (optional, 1-500 chars)
  - `description`: New description (optional, 0-5000 chars)
  - `completed`: New completion status (optional)

**Returns**:
- Updated Todo object if found and belongs to user
- `None` if not found or belongs to different user

**Behavior**:
- Filters by both `id` AND `user_id` (MANDATORY)
- Updates only provided fields (partial update)
- Updates `updated_at` to current UTC time
- Validates title if provided (not empty, length limits)
- Returns `None` if task doesn't exist or belongs to different user

**Errors**:
- `ValueError`: If title is empty or exceeds length limits
- `DatabaseError`: If database operation fails

**Example**:
```python
# Update task title
update_data = TodoUpdate(title="Buy groceries and cook dinner")
todo = await update_todo(session, "user-123", "task-uuid-456", update_data)
# Returns: Todo(...) with updated title and updated_at

# Try to update task belonging to different user
todo = await update_todo(session, "user-123", "other-user-task-uuid", update_data)
# Returns: None (prevents cross-user modification)
```

---

### 5. Delete Todo

**Function**: `delete_todo(session: AsyncSession, user_id: str, todo_id: str) -> bool`

**Purpose**: Delete a specific todo task with user ownership validation.

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user deleting the task (string)
- `todo_id`: ID of the task to delete (UUID string)

**Returns**:
- `True` if task was deleted
- `False` if task not found or belongs to different user

**Behavior**:
- Filters by both `id` AND `user_id` (MANDATORY)
- Permanently deletes the task from database
- Returns `False` if task doesn't exist or belongs to different user
- No soft delete (hard delete only)

**Errors**:
- `DatabaseError`: If database operation fails

**Example**:
```python
# Delete task that belongs to user
deleted = await delete_todo(session, "user-123", "task-uuid-456")
# Returns: True if deleted, False if not found

# Try to delete task belonging to different user
deleted = await delete_todo(session, "user-123", "other-user-task-uuid")
# Returns: False (prevents cross-user deletion)
```

---

### 6. Mark Complete (Helper)

**Function**: `mark_complete(session: AsyncSession, user_id: str, todo_id: str, completed: bool) -> Todo | None`

**Purpose**: Toggle completion status of a task (convenience wrapper around update).

**Parameters**:
- `session`: Database session (AsyncSession)
- `user_id`: ID of the user updating the task (string)
- `todo_id`: ID of the task to update (UUID string)
- `completed`: New completion status (boolean)

**Returns**:
- Updated Todo object if found and belongs to user
- `None` if not found or belongs to different user

**Behavior**:
- Filters by both `id` AND `user_id` (MANDATORY)
- Updates only `completed` field and `updated_at`
- Equivalent to `update_todo(session, user_id, todo_id, TodoUpdate(completed=completed))`

**Errors**:
- `DatabaseError`: If database operation fails

**Example**:
```python
# Mark task as complete
todo = await mark_complete(session, "user-123", "task-uuid-456", True)
# Returns: Todo(...) with completed=True

# Mark task as incomplete
todo = await mark_complete(session, "user-123", "task-uuid-456", False)
# Returns: Todo(...) with completed=False
```

---

## Security Guarantees

### User Isolation Enforcement

All operations MUST enforce user isolation through the following mechanisms:

1. **Query Filtering**: Every query includes `WHERE user_id = ?` clause
2. **Ownership Validation**: Update/delete operations verify ownership before modification
3. **No Information Leakage**: Operations return `None`/`False` for unauthorized access (don't reveal existence)
4. **Foreign Key Constraint**: `user_id` references valid user from auth system

### Example: Isolation in Action

```python
# User A creates a task
task_a = await create_todo(session, "user-a", TodoCreate(title="Task A"))
# task_a.id = "uuid-123"

# User B tries to access User A's task
task = await get_todo(session, "user-b", "uuid-123")
# Returns: None (User B cannot see User A's task)

# User B tries to update User A's task
updated = await update_todo(session, "user-b", "uuid-123", TodoUpdate(title="Hacked"))
# Returns: None (User B cannot modify User A's task)

# User B tries to delete User A's task
deleted = await delete_todo(session, "user-b", "uuid-123")
# Returns: False (User B cannot delete User A's task)
```

## Error Handling

### Database Errors

All operations should handle database errors gracefully:

```python
try:
    todo = await create_todo(session, user_id, todo_data)
except DatabaseError as e:
    # Log error
    logger.error(f"Database error creating todo: {e}")
    # Raise or return appropriate error response
    raise HTTPException(status_code=500, detail="Database error")
```

### Validation Errors

Field validation errors should be caught and returned as 400 Bad Request:

```python
try:
    todo_data = TodoCreate(title="")  # Empty title
except ValidationError as e:
    # Return 400 Bad Request with validation details
    raise HTTPException(status_code=400, detail=str(e))
```

## Performance Considerations

### Query Optimization

- **Index Usage**: All queries use `ix_todos_user_id` or `ix_todos_user_created` indexes
- **Pagination**: Use `skip`/`limit` to avoid loading all tasks
- **Selective Loading**: Load only needed fields when possible

### Connection Management

- **Session Lifecycle**: Use dependency injection for session management
- **Connection Pooling**: Reuse connections from pool (configured in database.py)
- **Transaction Scope**: Keep transactions short and focused

### Example: Efficient Pagination

```python
# Good: Paginated query
todos = await get_todos(session, user_id, skip=0, limit=20)

# Bad: Loading all tasks (avoid for users with many tasks)
todos = await get_todos(session, user_id, skip=0, limit=10000)
```

## Testing Contract

### Unit Tests

Each operation must have unit tests covering:

1. **Happy Path**: Operation succeeds with valid inputs
2. **User Isolation**: Operation respects user boundaries
3. **Edge Cases**: Empty results, invalid IDs, etc.
4. **Validation**: Field constraints enforced

### Integration Tests

Integration tests must verify:

1. **Cross-User Isolation**: User A cannot access User B's data
2. **Concurrent Operations**: Multiple users can operate simultaneously
3. **Transaction Integrity**: Operations are atomic and consistent

### Example Test Cases

```python
async def test_user_isolation():
    """Verify users cannot access each other's tasks."""
    # Create task for user A
    task_a = await create_todo(session, "user-a", TodoCreate(title="Task A"))

    # User B tries to get User A's task
    task = await get_todo(session, "user-b", task_a.id)
    assert task is None  # User B cannot see task

    # User B tries to update User A's task
    updated = await update_todo(session, "user-b", task_a.id, TodoUpdate(title="Hacked"))
    assert updated is None  # User B cannot modify task

    # User B tries to delete User A's task
    deleted = await delete_todo(session, "user-b", task_a.id)
    assert deleted is False  # User B cannot delete task
```

## Implementation Checklist

- [ ] All operations filter by `user_id`
- [ ] Update/delete operations validate ownership
- [ ] Operations return `None`/`False` for unauthorized access
- [ ] Field validation enforced (title, description lengths)
- [ ] Timestamps auto-managed (created_at, updated_at)
- [ ] Pagination supported (skip/limit parameters)
- [ ] Error handling implemented
- [ ] Unit tests written for each operation
- [ ] Integration tests verify user isolation
- [ ] Performance tests validate <100ms query latency

## Summary

This contract defines 6 core operations for user-scoped todo task management:

1. **create_todo**: Create new task
2. **get_todos**: List user's tasks (paginated)
3. **get_todo**: Get single task (with ownership check)
4. **update_todo**: Update task (with ownership check)
5. **delete_todo**: Delete task (with ownership check)
6. **mark_complete**: Toggle completion status (helper)

**Key Guarantees**:
- ✅ User isolation enforced at database level
- ✅ No cross-user data access possible
- ✅ All operations filter by user_id
- ✅ Ownership validated before modifications
- ✅ Performance optimized with indexes
