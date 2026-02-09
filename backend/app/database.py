from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.config import get_settings


def get_async_engine() -> AsyncEngine:
    """Create async engine for Neon PostgreSQL."""
    settings = get_settings()

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,  # Verify connections before using (serverless-safe)
        pool_size=5,         # Connection pool size
        max_overflow=10,     # Max connections beyond pool_size
        pool_recycle=3600,   # Recycle connections after 1 hour
    )
    return engine


# Create async engine
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
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise RuntimeError("Failed to connect to database. Please check DATABASE_URL configuration.")
