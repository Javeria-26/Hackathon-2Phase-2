from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_session
from app.auth import get_current_user_id
from app.models import TodoCreate, TodoUpdate, TodoResponse
from app import crud


router = APIRouter()


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Create a new todo for the authenticated user."""
    todo = await crud.create_todo(session, todo_data, current_user_id)
    return todo


@router.get("/todos", response_model=List[TodoResponse])
async def list_todos(
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get all todos for the authenticated user with optional filters."""
    todos = await crud.get_todos_by_user(
        session,
        current_user_id,
        completed=completed,
        search=search
    )
    return todos


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific todo by ID."""
    todo = await crud.get_todo_by_id(session, todo_id, current_user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Update an existing todo."""
    todo = await crud.get_todo_by_id(session, todo_id, current_user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    updated_todo = await crud.update_todo(session, todo, todo_data)
    return updated_todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Delete a todo."""
    todo = await crud.get_todo_by_id(session, todo_id, current_user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    await crud.delete_todo(session, todo)
    return None
