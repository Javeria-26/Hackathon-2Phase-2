# Quick Start: Neon PostgreSQL Setup

**Feature**: 001-neon-postgres-todos
**Date**: 2026-02-09
**Purpose**: Setup guide for Neon PostgreSQL database layer

## Prerequisites

- Python 3.11+
- Neon PostgreSQL account and database instance
- FastAPI backend project (existing)

## Step 1: Provision Neon Database

### Create Neon Project

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Note your connection details:
   - Host: `<project-id>.neon.tech`
   - Database name: `neondb` (default)
   - Username: Your Neon username
   - Password: Your Neon password

### Get Connection String

From Neon dashboard, copy the connection string:
```
postgresql://username:password@project-id.neon.tech/neondb?sslmode=require
```

## Step 2: Install Dependencies

### Add asyncpg Driver

Update `backend/requirements.txt`:
```txt
# Existing dependencies
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14

# Add PostgreSQL async driver
asyncpg==0.29.0
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 3: Configure Environment

### Update .env File

Edit `backend/.env`:
```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@project-id.neon.tech/neondb?sslmode=require

# JWT Configuration (existing)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# CORS Configuration (existing)
FRONTEND_URL=http://localhost:3000

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

**Important**:
- Replace `username`, `password`, and `project-id` with your Neon credentials
- Keep `?sslmode=require` - Neon requires SSL connections
- Use `postgresql+asyncpg://` prefix for async driver

### Update .env.example

Update `backend/.env.example` for documentation:
```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

## Step 4: Update Database Configuration

### Verify database.py

Ensure `backend/app/database.py` has correct pooling configuration:

```python
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

def get_async_engine() -> AsyncEngine:
    """Create async engine for Neon PostgreSQL."""
    settings = get_settings()

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,      # Verify connections before use
        pool_size=5,             # Base connection pool
        max_overflow=10,         # Burst capacity
        pool_recycle=3600,       # Recycle after 1 hour
    )
    return engine
```

**Key Parameters**:
- `pool_pre_ping=True`: Detects stale connections (essential for serverless)
- `pool_size=5`: Conservative base pool size
- `max_overflow=10`: Allows bursts up to 15 total connections
- `pool_recycle=3600`: Prevents idle connection timeouts

## Step 5: Update Models

### Verify Todo Model

Ensure `backend/app/models.py` uses correct field constraints:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Todo(SQLModel, table=True):
    """Database model for Todo."""
    __tablename__ = "todos"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(min_length=1, max_length=500, nullable=False)
    description: str = Field(default="", max_length=5000)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

**Key Changes from SQLite**:
- UUID primary key (was auto-increment in SQLite)
- Explicit `nullable=False` for required fields
- Field length constraints (title: 500, description: 5000)

## Step 6: Create Database Schema

### Run Schema Creation

The schema is automatically created on application startup via `create_db_and_tables()` in `main.py`:

```python
from app.database import create_db_and_tables

@app.on_event("startup")
async def on_startup():
    """Initialize database on startup."""
    await create_db_and_tables()
```

### Manual Schema Creation (if needed)

If you need to create schema manually:

```bash
cd backend
python -c "
import asyncio
from app.database import create_db_and_tables

asyncio.run(create_db_and_tables())
print('Database schema created successfully')
"
```

## Step 7: Verify Connection

### Test Database Connection

Create a test script `backend/test_connection.py`:

```python
import asyncio
from app.database import engine
from sqlalchemy import text

async def test_connection():
    """Test Neon PostgreSQL connection."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL: {version}")

            # Test table exists
            result = await conn.execute(
                text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'todos'")
            )
            count = result.scalar()
            if count > 0:
                print("✅ 'todos' table exists")
            else:
                print("⚠️  'todos' table not found - run schema creation")

    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run the test:
```bash
python test_connection.py
```

Expected output:
```
✅ Connected to PostgreSQL: PostgreSQL 15.x on x86_64-pc-linux-gnu
✅ 'todos' table exists
```

## Step 8: Run Application

### Start FastAPI Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Endpoints

Test the API:
```bash
# Health check
curl http://localhost:8000/

# Create a todo (requires authentication)
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"title": "Test Task", "description": "Testing Neon PostgreSQL"}'
```

## Step 9: Run Tests

### Run Test Suite

```bash
cd backend
pytest tests/ -v
```

Expected tests:
- `test_todos.py`: CRUD operations
- `test_isolation.py`: User data isolation
- `test_concurrent.py`: Concurrent operations (if implemented)

### Verify Test Results

All tests should pass:
```
tests/test_todos.py::test_create_todo PASSED
tests/test_todos.py::test_get_todos PASSED
tests/test_todos.py::test_update_todo PASSED
tests/test_todos.py::test_delete_todo PASSED
tests/test_isolation.py::test_user_isolation PASSED
```

## Troubleshooting

### Connection Refused

**Error**: `Connection refused` or `could not connect to server`

**Solutions**:
1. Verify DATABASE_URL is correct
2. Check Neon project is active (not suspended)
3. Verify SSL mode: `?sslmode=require`
4. Check firewall/network settings

### SSL Required

**Error**: `SSL connection is required`

**Solution**: Ensure connection string includes `?sslmode=require`

### Authentication Failed

**Error**: `password authentication failed`

**Solutions**:
1. Verify username and password in DATABASE_URL
2. Reset password in Neon dashboard if needed
3. Check for special characters in password (URL encode if needed)

### Connection Pool Exhausted

**Error**: `QueuePool limit exceeded`

**Solutions**:
1. Increase `max_overflow` in database.py
2. Check for connection leaks (ensure sessions are closed)
3. Reduce concurrent requests
4. Upgrade Neon tier for more connections

### Schema Not Created

**Error**: `relation "todos" does not exist`

**Solutions**:
1. Run `create_db_and_tables()` manually
2. Check application startup logs for errors
3. Verify DATABASE_URL points to correct database
4. Check user has CREATE TABLE permissions

## Performance Tuning

### Connection Pool Sizing

For production, adjust based on load:

```python
# Low traffic (< 100 req/min)
pool_size=5, max_overflow=10

# Medium traffic (100-1000 req/min)
pool_size=10, max_overflow=20

# High traffic (> 1000 req/min)
pool_size=20, max_overflow=30
```

### Query Optimization

Monitor slow queries:
```python
# Enable SQL logging in development
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # Logs all SQL queries
)
```

### Index Verification

Check indexes are created:
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'todos';
```

Expected indexes:
- `todos_pkey` (primary key on id)
- `ix_todos_user_id` (index on user_id)

## Security Checklist

- [ ] DATABASE_URL stored in .env (not committed to git)
- [ ] .env added to .gitignore
- [ ] SSL mode enabled (`?sslmode=require`)
- [ ] Connection pooling configured
- [ ] User isolation enforced in all queries
- [ ] Field validation enabled (title, description lengths)
- [ ] JWT authentication required for all endpoints

## Next Steps

1. **Test CRUD Operations**: Verify all create, read, update, delete operations work
2. **Test User Isolation**: Ensure users cannot access each other's tasks
3. **Performance Testing**: Validate <100ms query latency for 1000 tasks
4. **Integration Testing**: Test with frontend application
5. **Monitoring**: Set up logging and monitoring for production

## Resources

- [Neon Documentation](https://neon.tech/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
