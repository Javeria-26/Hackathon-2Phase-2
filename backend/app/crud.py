from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import Todo, TodoCreate, TodoUpdate
from typing import List, Optional
from datetime import datetime


async def create_todo(
    session: AsyncSession,
    user_id: str,
    todo_data: TodoCreate
) -> Todo:
    """
    Create a new todo for a user.

    Args:
        session: Database session
        user_id: ID of the user creating the task
        todo_data: Todo creation data

    Returns:
        Created Todo object

    Raises:
        ValueError: If user_id is None or empty
        SQLAlchemyError: If database operation fails
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be None or empty")

    try:
        todo = Todo(
            **todo_data.model_dump(),
            user_id=user_id.strip()
        )
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        await session.rollback()
        raise SQLAlchemyError(f"Database error creating todo: {str(e)}")


async def get_todos(
    session: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Todo]:
    """
    Get all todos for a user, ordered by creation date (newest first).

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return

    Returns:
        List of Todo objects (may be empty)

    Raises:
        ValueError: If user_id is None or empty
        SQLAlchemyError: If database operation fails
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be None or empty")

    try:
        query = select(Todo).where(
            Todo.user_id == user_id.strip()
        ).order_by(
            Todo.created_at.desc()
        ).offset(skip).limit(limit)

        result = await session.execute(query)
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Database error retrieving todos: {str(e)}")


async def get_todo(
    session: AsyncSession,
    user_id: str,
    todo_id: str
) -> Optional[Todo]:
    """
    Get a specific todo by ID, with user ownership validation.

    Args:
        session: Database session
        user_id: ID of the user requesting the task
        todo_id: ID of the task to retrieve

    Returns:
        Todo object if found and belongs to user, None otherwise

    Raises:
        ValueError: If user_id or todo_id is None or empty
        SQLAlchemyError: If database operation fails
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be None or empty")
    if not todo_id or not todo_id.strip():
        raise ValueError("todo_id cannot be None or empty")

    try:
        query = select(Todo).where(
            Todo.id == todo_id.strip(),
            Todo.user_id == user_id.strip()
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Database error retrieving todo: {str(e)}")


async def update_todo(
    session: AsyncSession,
    user_id: str,
    todo_id: str,
    todo_data: TodoUpdate
) -> Optional[Todo]:
    """
    Update a specific todo with user ownership validation.

    Args:
        session: Database session
        user_id: ID of the user updating the task
        todo_id: ID of the task to update
        todo_data: Update data

    Returns:
        Updated Todo object if found and belongs to user, None otherwise

    Raises:
        ValueError: If user_id or todo_id is None or empty, or validation fails
        SQLAlchemyError: If database operation fails
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be None or empty")
    if not todo_id or not todo_id.strip():
        raise ValueError("todo_id cannot be None or empty")

    try:
        # Get the todo with ownership check
        todo = await get_todo(session, user_id, todo_id)
        if not todo:
            return None

        # Update fields
        for key, value in todo_data.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)

        todo.updated_at = datetime.utcnow()
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo
    except ValueError:
        raise
    except SQLAlchemyError as e:
        await session.rollback()
        raise SQLAlchemyError(f"Database error updating todo: {str(e)}")


async def delete_todo(
    session: AsyncSession,
    user_id: str,
    todo_id: str
) -> bool:
    """
    Delete a specific todo with user ownership validation.

    Args:
        session: Database session
        user_id: ID of the user deleting the task
        todo_id: ID of the task to delete

    Returns:
        True if task was deleted, False if not found or belongs to different user

    Raises:
        ValueError: If user_id or todo_id is None or empty
        SQLAlchemyError: If database operation fails
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be None or empty")
    if not todo_id or not todo_id.strip():
        raise ValueError("todo_id cannot be None or empty")

    try:
        # Get the todo with ownership check
        todo = await get_todo(session, user_id, todo_id)
        if not todo:
            return False

        await session.delete(todo)
        await session.commit()
        return True
    except ValueError:
        raise
    except SQLAlchemyError as e:
        await session.rollback()
        raise SQLAlchemyError(f"Database error deleting todo: {str(e)}")


async def mark_complete(
    session: AsyncSession,
    user_id: str,
    todo_id: str,
    completed: bool
) -> Optional[Todo]:
    """
    Toggle completion status of a task (convenience wrapper around update).

    Args:
        session: Database session
        user_id: ID of the user updating the task
        todo_id: ID of the task to update
        completed: New completion status

    Returns:
        Updated Todo object if found and belongs to user, None otherwise

    Raises:
        ValueError: If user_id or todo_id is None or empty
        SQLAlchemyError: If database operation fails
    """
    todo_data = TodoUpdate(completed=completed)
    return await update_todo(session, user_id, todo_id, todo_data)
