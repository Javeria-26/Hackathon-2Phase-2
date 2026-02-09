from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator
import uuid


class TodoBase(SQLModel):
    """Base model for Todo with shared fields."""
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)
    completed: bool = Field(default=False)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    @field_validator('description')
    @classmethod
    def description_clean(cls, v: str) -> str:
        """Clean description whitespace."""
        return v.strip()


class Todo(TodoBase, table=True):
    """Database model for Todo."""
    __tablename__ = "todos"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(index=True)  # Indexed for fast user-scoped queries
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoCreate(TodoBase):
    """Schema for creating a todo."""
    pass


class TodoUpdate(SQLModel):
    """Schema for updating a todo (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else v


class TodoResponse(TodoBase):
    """Schema for todo response."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
