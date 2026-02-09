from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Todo, TodoCreate, TodoUpdate
from typing import List, Optional
from datetime import datetime


async def get_todos_by_user(
    session: AsyncSession,
    user_id: str,
    completed: Optional[bool] = None,
    search: Optional[str] = None
) -> List[Todo]:
    """
    Get all todos for a user with optional filters.
    """
    query = select(Todo).where(Todo.user_id == user_id)

    # Apply filters
    if completed is not None:
        query = query.where(Todo.completed == completed)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Todo.title.ilike(search_pattern)) |
            (Todo.description.ilike(search_pattern))
        )

    # Order by creation date (newest first)
    query = query.order_by(Todo.created_at.desc())

    result = await session.execute(query)
    return result.scalars().all()


async def get_todo_by_id(
    session: AsyncSession,
    todo_id: str,
    user_id: str
) -> Optional[Todo]:
    """
    Get a specific todo by ID, ensuring it belongs to the user.
    """
    query = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == user_id
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_todo(
    session: AsyncSession,
    todo_data: TodoCreate,
    user_id: str
) -> Todo:
    """
    Create a new todo for a user.
    """
    todo = Todo(
        **todo_data.model_dump(),
        user_id=user_id
    )
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def update_todo(
    session: AsyncSession,
    todo: Todo,
    todo_data: TodoUpdate
) -> Todo:
    """
    Update an existing todo.
    """
    for key, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def delete_todo(
    session: AsyncSession,
    todo: Todo
) -> None:
    """
    Delete a todo.
    """
    await session.delete(todo)
    await session.commit()
