import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from jose import jwt
from datetime import datetime, timedelta
from app.main import app
from app.database import get_session
from app.config import get_settings


# In-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(name="engine")
async def engine_fixture():
    """Create test database engine."""
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
    """Create test database session."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    """Create test client with overridden dependencies."""
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="test_user_id")
def test_user_id_fixture():
    """Test user ID."""
    return "test-user-123"


@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user_id):
    """Generate valid JWT token for testing."""
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
    """Authorization headers for testing."""
    return {"Authorization": f"Bearer {auth_token}"}
