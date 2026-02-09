# Research Document: FastAPI Todo Backend

**Feature**: 003-fastapi-todo-backend
**Date**: 2026-02-09
**Status**: Complete

---

## Executive Summary

This document provides production-ready recommendations for implementing a secure FastAPI backend that verifies JWT tokens from Better Auth and manages user-scoped todos with Neon PostgreSQL. All recommendations are based on analysis of the existing frontend implementation and industry best practices.

---

## 1. JWT Verification in FastAPI

### Recommended Library: python-jose

**Decision**: Use `python-jose[cryptography]` for JWT verification.

**Rationale**:
- Most widely adopted in FastAPI ecosystem
- Excellent documentation and community support
- Built-in support for multiple algorithms (HS256, RS256, etc.)
- Type-safe with proper error handling
- Actively maintained

**Installation**:
```bash
pip install "python-jose[cryptography]" python-multipart
```

### Implementation Pattern

#### 1. JWT Configuration (config.py)

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_HOURS: int = 24

    # Database Configuration
    DATABASE_URL: str

    # CORS Configuration
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
```

#### 2. JWT Dependency (auth.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from config import get_settings

security = HTTPBearer()

class TokenData:
    """Parsed JWT token data"""
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Verify JWT token and extract user information.

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing required claims
    """
    settings = get_settings()
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user ID from token claims
        user_id: Optional[str] = payload.get("sub") or payload.get("userId")
        email: Optional[str] = payload.get("email")

        if user_id is None:
            raise credentials_exception

        return TokenData(user_id=user_id, email=email or "")

    except JWTError as e:
        # Log the error for debugging (don't expose to client)
        print(f"JWT verification failed: {str(e)}")
        raise credentials_exception

async def get_current_user_id(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Extract user ID from verified token.
    Use this as a dependency in route handlers.
    """
    return token_data.user_id
```

#### 3. Usage in Route Handlers

```python
from fastapi import APIRouter, Depends
from auth import get_current_user_id

router = APIRouter()

@router.get("/todos")
async def get_todos(current_user_id: str = Depends(get_current_user_id)):
    """
    Get all todos for authenticated user.
    current_user_id is automatically extracted from JWT token.
    """
    # Query todos filtered by current_user_id
    pass

@router.post("/todos")
async def create_todo(
    todo_data: TodoCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create todo for authenticated user.
    """
    # Create todo with user_id = current_user_id
    pass
```

### Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError

@app.exception_handler(JWTError)
async def jwt_exception_handler(request: Request, exc: JWTError):
    """Global handler for JWT errors"""
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Invalid or expired authentication token"
            }
        }
    )
```

---

## 2. Better Auth JWT Token Structure

### Analysis of Frontend Implementation

Based on the frontend code analysis (`E:\NewFolder\Hackathon2\Phase 2\frontend\lib\auth\better-auth.ts`):

**Better Auth Configuration**:
- Session expiration: 24 hours (86400 seconds)
- Algorithm: HS256 (default)
- Secret: Shared between frontend and backend via `BETTER_AUTH_SECRET`

### JWT Token Claims

Better Auth uses standard JWT claims with the following structure:

```typescript
{
  // Standard JWT claims
  "iat": 1707390000,        // Issued at (Unix timestamp)
  "exp": 1707476400,        // Expiration (Unix timestamp)

  // Better Auth user claims
  "sub": "user-id-here",    // Subject (user ID) - PRIMARY
  "userId": "user-id-here", // Alternative user ID claim
  "email": "user@example.com",
  "name": "User Name"       // Optional
}
```

### Key Findings

1. **User ID Claim**: Better Auth may use either `sub` (standard JWT claim) or `userId` (custom claim)
2. **Recommendation**: Check both `sub` and `userId` claims for maximum compatibility
3. **Email Claim**: Always present in Better Auth tokens
4. **Session Duration**: 24 hours from issuance

### Backend Verification Strategy

```python
def extract_user_id_from_token(payload: dict) -> str:
    """
    Extract user ID from Better Auth JWT token.
    Checks both 'sub' (standard) and 'userId' (Better Auth custom) claims.
    """
    user_id = payload.get("sub") or payload.get("userId")
    if not user_id:
        raise ValueError("Token missing user ID claim")
    return user_id
```

---

## 3. SQLModel with Neon PostgreSQL

### Recommended Approach: Async SQLModel with asyncpg

**Libraries**:
```bash
pip install sqlmodel asyncpg psycopg2-binary
```

### Database Configuration

#### 1. Connection Setup (database.py)

```python
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from config import get_settings

# Create async engine for Neon PostgreSQL
def get_async_engine() -> AsyncEngine:
    settings = get_settings()

    # Neon PostgreSQL connection string format:
    # postgresql+asyncpg://user:password@host/database?sslmode=require

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # Set to False in production
        future=True,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,         # Connection pool size
        max_overflow=10,     # Max connections beyond pool_size
        pool_recycle=3600,   # Recycle connections after 1 hour
    )
    return engine

engine = get_async_engine()

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.
    Automatically handles session lifecycle.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_db_and_tables():
    """
    Create database tables.
    Call this on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

#### 2. Model Definition (models.py)

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TodoBase(SQLModel):
    """Base model for Todo with shared fields"""
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    """Database model for Todo"""
    __tablename__ = "todos"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(index=True)  # Indexed for fast queries
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    """Schema for creating a todo"""
    pass

class TodoUpdate(TodoBase):
    """Schema for updating a todo"""
    pass

class TodoResponse(TodoBase):
    """Schema for todo response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### 3. Database Operations (crud.py)

```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Todo, TodoCreate, TodoUpdate
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
```

#### 4. Route Handler Integration

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from auth import get_current_user_id
import crud
from models import TodoCreate, TodoResponse

router = APIRouter()

@router.get("/todos", response_model=List[TodoResponse])
async def list_todos(
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get all todos for authenticated user"""
    todos = await crud.get_todos_by_user(
        session,
        current_user_id,
        completed=completed,
        search=search
    )
    return todos

@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Create a new todo"""
    todo = await crud.create_todo(session, todo_data, current_user_id)
    return todo
```

### Neon PostgreSQL Specific Considerations

1. **Connection String Format**:
   ```
   postgresql+asyncpg://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

2. **SSL Required**: Neon requires SSL connections (`sslmode=require`)

3. **Connection Pooling**: Use moderate pool sizes (5-10) for serverless environments

4. **Idle Timeout**: Neon may close idle connections; use `pool_pre_ping=True`

5. **Serverless Optimization**: Keep connections short-lived, use connection pooling

---

## 4. FastAPI Best Practices

### CORS Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings

app = FastAPI(title="Todo API", version="1.0.0")

settings = get_settings()

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Specific origin, not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

### Error Handling

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    errors = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])  # Skip 'body'
        errors[field] = error["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": errors
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    # Log the error (use proper logging in production)
    print(f"Unexpected error: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
```

### Request/Response Validation

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    @field_validator('description')
    @classmethod
    def description_clean(cls, v: str) -> str:
        return v.strip()
```

### Dependency Injection Pattern

```python
from fastapi import Depends, HTTPException, status
from typing import Annotated

# Type alias for cleaner code
CurrentUser = Annotated[str, Depends(get_current_user_id)]
DBSession = Annotated[AsyncSession, Depends(get_session)]

@router.get("/todos/{todo_id}")
async def get_todo(
    todo_id: str,
    current_user: CurrentUser,
    session: DBSession
):
    """
    Cleaner route handler with type aliases.
    Dependencies are automatically injected.
    """
    todo = await crud.get_todo_by_id(session, todo_id, current_user)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo
```

### Application Lifecycle

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    Runs on startup and shutdown.
    """
    # Startup
    print("Creating database tables...")
    await create_db_and_tables()
    print("Application started")

    yield

    # Shutdown
    print("Closing database connections...")
    await engine.dispose()
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)
```

---

## 5. Testing Strategy

### Testing Stack

```bash
pip install pytest pytest-asyncio httpx
```

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
├── test_todos.py         # Todo CRUD tests
└── test_integration.py   # End-to-end tests
```

### Fixtures (conftest.py)

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from jose import jwt
from datetime import datetime, timedelta
from main import app
from database import get_session
from config import get_settings

# In-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(name="engine")
async def engine_fixture():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture(name="session")
async def session_fixture(engine):
    """Create test database session"""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    """Create test client with overridden dependencies"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()

@pytest.fixture(name="test_user_id")
def test_user_id_fixture():
    """Test user ID"""
    return "test-user-123"

@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user_id):
    """Generate valid JWT token for testing"""
    settings = get_settings()

    payload = {
        "sub": test_user_id,
        "email": "test@example.com",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token

@pytest.fixture(name="auth_headers")
def auth_headers_fixture(auth_token):
    """Authorization headers for testing"""
    return {"Authorization": f"Bearer {auth_token}"}
```

### Authentication Tests (test_auth.py)

```python
import pytest
from fastapi import status

def test_missing_token(client):
    """Test request without authentication token"""
    response = client.get("/todos")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_invalid_token(client):
    """Test request with invalid token"""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/todos", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_expired_token(client, test_user_id):
    """Test request with expired token"""
    from jose import jwt
    from datetime import datetime, timedelta
    from config import get_settings

    settings = get_settings()

    # Create expired token
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/todos", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_valid_token(client, auth_headers):
    """Test request with valid token"""
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
```

### Todo CRUD Tests (test_todos.py)

```python
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_todo(client, auth_headers):
    """Test creating a todo"""
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }

    response = client.post("/todos", json=todo_data, headers=auth_headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_list_todos(client, auth_headers):
    """Test listing todos"""
    # Create a todo first
    client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test"},
        headers=auth_headers
    )

    # List todos
    response = client.get("/todos", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_user_isolation(client, auth_token, test_user_id):
    """Test that users can only see their own todos"""
    # Create todo for user 1
    headers_user1 = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/todos",
        json={"title": "User 1 Todo"},
        headers=headers_user1
    )
    todo_id = response.json()["id"]

    # Create token for user 2
    from jose import jwt
    from datetime import datetime, timedelta
    from config import get_settings

    settings = get_settings()
    payload = {
        "sub": "different-user-456",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token_user2 = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    # User 2 tries to access User 1's todo
    response = client.get(f"/todos/{todo_id}", headers=headers_user2)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_validation_errors(client, auth_headers):
    """Test input validation"""
    # Empty title
    response = client.post(
        "/todos",
        json={"title": "", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Title too long
    response = client.post(
        "/todos",
        json={"title": "x" * 201, "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run async tests
pytest -v --asyncio-mode=auto
```

---

## 6. Environment Configuration

### .env File Template

```bash
# JWT Configuration (MUST match frontend BETTER_AUTH_SECRET)
JWT_SECRET_KEY=your-secret-key-here-min-32-characters-change-in-production
JWT_ALGORITHM=HS256

# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

### Production Considerations

1. **Secret Management**: Use environment variables, never commit secrets
2. **Database URL**: Use connection pooling for Neon PostgreSQL
3. **CORS**: Set specific frontend origin, not "*"
4. **Logging**: Use structured logging (e.g., structlog)
5. **Monitoring**: Add health check endpoints
6. **Rate Limiting**: Consider adding rate limiting middleware

---

## 7. Project Structure Recommendation

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings and configuration
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLModel models
│   ├── auth.py              # JWT verification and dependencies
│   ├── crud.py              # Database operations
│   └── routers/
│       ├── __init__.py
│       └── todos.py         # Todo endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Auth tests
│   └── test_todos.py        # Todo tests
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md                # Setup instructions
```

---

## 8. Dependencies (requirements.txt)

```txt
# FastAPI and server
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlmodel==0.0.14
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Configuration
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0

# Development
black==24.1.1
ruff==0.1.14
```

---

## 9. Quick Start Implementation Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file with JWT_SECRET_KEY matching frontend
- [ ] Set up Neon PostgreSQL database and get connection string
- [ ] Implement database models (models.py)
- [ ] Implement JWT verification (auth.py)
- [ ] Implement CRUD operations (crud.py)
- [ ] Implement API routes (routers/todos.py)
- [ ] Configure CORS for frontend origin
- [ ] Add error handlers
- [ ] Write tests for authentication
- [ ] Write tests for todo CRUD operations
- [ ] Test user isolation (users can only access their own todos)
- [ ] Run application: `uvicorn app.main:app --reload`
- [ ] Verify integration with frontend

---

## 10. Key Takeaways

1. **JWT Verification**: Use python-jose with HS256 algorithm, check both `sub` and `userId` claims
2. **Better Auth Compatibility**: Shared secret must match frontend `BETTER_AUTH_SECRET`
3. **Database**: Use async SQLModel with asyncpg for Neon PostgreSQL
4. **Connection Pooling**: Configure moderate pool sizes (5-10) for serverless
5. **Security**: Always verify user_id from JWT matches path parameters
6. **Testing**: Mock JWT tokens in tests, use in-memory SQLite for test database
7. **Error Handling**: Return consistent error format matching frontend expectations
8. **CORS**: Configure specific origin, enable credentials
9. **Validation**: Use Pydantic models for request/response validation
10. **Production**: Use environment variables, structured logging, health checks

---

**Status**: Research complete, ready for implementation planning
