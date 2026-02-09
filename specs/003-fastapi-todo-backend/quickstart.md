# Quickstart Guide: FastAPI Todo Backend

**Feature**: 003-fastapi-todo-backend
**Date**: 2026-02-09

---

## Overview

This guide provides step-by-step instructions to set up and run the FastAPI Todo Backend locally for development and testing.

**Prerequisites**:
- Python 3.11 or higher
- pip (Python package manager)
- Neon PostgreSQL database (or local PostgreSQL)
- Better Auth JWT secret (from frontend)

---

## 1. Project Setup

### Clone and Navigate

```bash
cd backend
```

### Create Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected dependencies** (see `requirements.txt`):
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- sqlmodel==0.0.14
- asyncpg==0.29.0
- python-jose[cryptography]==3.3.0
- pydantic-settings==2.1.0
- pytest==7.4.4
- pytest-asyncio==0.23.3
- httpx==0.26.0

---

## 2. Environment Configuration

### Create .env File

Copy the example environment file:

```bash
cp .env.example .env
```

### Configure Environment Variables

Edit `.env` with your settings:

```bash
# JWT Configuration (MUST match frontend BETTER_AUTH_SECRET)
JWT_SECRET_KEY=your-secret-key-here-min-32-characters-change-in-production
JWT_ALGORITHM=HS256

# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

**Important Notes**:
- `JWT_SECRET_KEY` MUST match the `BETTER_AUTH_SECRET` from your frontend `.env`
- `DATABASE_URL` must use `postgresql+asyncpg://` prefix for async support
- `DATABASE_URL` must include `?sslmode=require` for Neon PostgreSQL
- `FRONTEND_URL` should match your frontend development server

### Get Neon PostgreSQL Connection String

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project or select existing project
3. Navigate to "Connection Details"
4. Copy the connection string
5. Replace `postgresql://` with `postgresql+asyncpg://`
6. Add `?sslmode=require` at the end

**Example**:
```
postgresql+asyncpg://user:password@ep-cool-mountain-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

---

## 3. Database Setup

The database tables will be created automatically on first run using SQLModel's `create_all()` method.

**Manual verification** (optional):

```bash
# Connect to your Neon database
psql "postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"

# Check if todos table exists
\dt

# View table schema
\d todos
```

---

## 4. Running the Application

### Development Server

Start the FastAPI development server with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Creating database tables...
Application started
INFO:     Application startup complete.
```

### Verify Server is Running

Open your browser and navigate to:

- **API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 5. Testing the API

### Using Swagger UI (Recommended for Development)

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your JWT token: `Bearer <your-token>`
4. Try the endpoints interactively

### Using curl

**Get JWT Token from Frontend**:
1. Log in to your frontend application
2. Open browser DevTools → Application → Local Storage
3. Find the JWT token (usually stored as `auth_token` or similar)

**List Todos**:
```bash
curl -X GET "http://localhost:8000/todos" \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Create Todo**:
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Todo",
    "description": "Testing the API"
  }'
```

**Get Specific Todo**:
```bash
curl -X GET "http://localhost:8000/todos/{todo-id}" \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Update Todo**:
```bash
curl -X PUT "http://localhost:8000/todos/{todo-id}" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Todo",
    "completed": true
  }'
```

**Delete Todo**:
```bash
curl -X DELETE "http://localhost:8000/todos/{todo-id}" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Using Python Requests

```python
import requests

# Your JWT token from frontend
token = "your-jwt-token-here"
headers = {"Authorization": f"Bearer {token}"}

# List todos
response = requests.get("http://localhost:8000/todos", headers=headers)
print(response.json())

# Create todo
todo_data = {"title": "Test Todo", "description": "Testing"}
response = requests.post("http://localhost:8000/todos", json=todo_data, headers=headers)
print(response.json())
```

---

## 6. Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_todos.py
pytest tests/test_isolation.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Async Tests

```bash
pytest -v --asyncio-mode=auto
```

---

## 7. Common Issues and Troubleshooting

### Issue: "Invalid or expired authentication token"

**Cause**: JWT secret mismatch between frontend and backend

**Solution**:
1. Check that `JWT_SECRET_KEY` in backend `.env` matches `BETTER_AUTH_SECRET` in frontend `.env`
2. Ensure both are at least 32 characters long
3. Restart both frontend and backend after changing secrets

### Issue: "Connection refused" or database errors

**Cause**: Database connection issues

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Ensure `?sslmode=require` is included for Neon
3. Check that database is accessible (not paused in Neon)
4. Test connection with `psql` command

### Issue: CORS errors in browser

**Cause**: CORS not configured correctly

**Solution**:
1. Verify `FRONTEND_URL` in `.env` matches your frontend URL exactly
2. Ensure no trailing slash in `FRONTEND_URL`
3. Restart backend after changing CORS settings

### Issue: "Module not found" errors

**Cause**: Dependencies not installed or virtual environment not activated

**Solution**:
1. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Verify installation: `pip list`

### Issue: Tests failing with database errors

**Cause**: Test database configuration issues

**Solution**:
1. Tests use in-memory SQLite, no external database needed
2. Ensure `pytest-asyncio` is installed
3. Run with `--asyncio-mode=auto` flag

---

## 8. Development Workflow

### Making Changes

1. **Edit code** in `app/` directory
2. **Server auto-reloads** (if using `--reload` flag)
3. **Test changes** using Swagger UI or curl
4. **Run tests** to verify functionality
5. **Commit changes** with descriptive message

### Adding New Endpoints

1. Define route in `app/routers/todos.py`
2. Add CRUD operation in `app/crud.py` if needed
3. Update OpenAPI spec in `specs/003-fastapi-todo-backend/contracts/openapi.yaml`
4. Write tests in `tests/`
5. Update documentation

### Database Schema Changes

1. Modify models in `app/models.py`
2. Create migration script (if using Alembic)
3. Test migration on development database
4. Update `data-model.md` documentation

---

## 9. Production Deployment

### Environment Variables

Set production environment variables:

```bash
JWT_SECRET_KEY=<strong-random-secret-min-32-chars>
DATABASE_URL=<neon-production-connection-string>
FRONTEND_URL=https://your-frontend-domain.com
ENVIRONMENT=production
DEBUG=false
```

### Running in Production

**Using Uvicorn**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Using Gunicorn with Uvicorn workers**:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t todo-api .
docker run -p 8000:8000 --env-file .env todo-api
```

---

## 10. API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### OpenAPI Specification

- **JSON**: http://localhost:8000/openapi.json
- **YAML**: `specs/003-fastapi-todo-backend/contracts/openapi.yaml`

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | List all todos (with filters) |
| POST | `/todos` | Create new todo |
| GET | `/todos/{id}` | Get specific todo |
| PUT | `/todos/{id}` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |

---

## 11. Next Steps

1. **Integrate with Frontend**: Update frontend API client to point to `http://localhost:8000`
2. **Test End-to-End**: Create, read, update, delete todos from frontend
3. **Verify User Isolation**: Log in as different users and verify data separation
4. **Performance Testing**: Test with multiple concurrent requests
5. **Deploy to Production**: Follow production deployment steps above

---

## 12. Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code (if using black)
black app/ tests/

# Lint code (if using ruff)
ruff check app/ tests/

# Check types (if using mypy)
mypy app/

# Generate requirements.txt
pip freeze > requirements.txt
```

---

## Support

For issues or questions:
- Check the [API documentation](http://localhost:8000/docs)
- Review [data-model.md](./data-model.md) for database schema
- Review [plan.md](./plan.md) for architecture decisions
- Review [research.md](./research.md) for implementation patterns
