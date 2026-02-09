# FastAPI Todo Backend

A secure REST API for user-scoped todo management with JWT authentication.

## Features

- ✅ JWT authentication with Better Auth integration
- ✅ User-scoped data isolation
- ✅ Complete CRUD operations for todos
- ✅ Filtering by completion status
- ✅ Text search in title and description
- ✅ Async SQLModel with PostgreSQL
- ✅ Comprehensive test suite

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL database
- Better Auth JWT secret (from frontend)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# MUST match frontend BETTER_AUTH_SECRET
JWT_SECRET_KEY=your-secret-key-here-min-32-characters

# Neon PostgreSQL connection string
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=true
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/todos` | Create a new todo |
| GET | `/todos` | List all todos (with optional filters) |
| GET | `/todos/{id}` | Get a specific todo |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

### Query Parameters

- `completed` (boolean): Filter by completion status
- `search` (string): Search in title and description

### Example Requests

**Create Todo:**
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**List Todos:**
```bash
curl -X GET "http://localhost:8000/todos" \
  -H "Authorization: Bearer <token>"
```

**Filter Completed Todos:**
```bash
curl -X GET "http://localhost:8000/todos?completed=true" \
  -H "Authorization: Bearer <token>"
```

**Search Todos:**
```bash
curl -X GET "http://localhost:8000/todos?search=meeting" \
  -H "Authorization: Bearer <token>"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_todos.py

# Run with verbose output
pytest -v
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, error handlers
│   ├── config.py            # Environment configuration
│   ├── database.py          # Async database setup
│   ├── models.py            # SQLModel models
│   ├── auth.py              # JWT verification
│   ├── crud.py              # Database operations
│   └── routers/
│       └── todos.py         # Todo endpoints
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Authentication tests
│   ├── test_todos.py        # CRUD tests
│   └── test_isolation.py    # User isolation tests
├── .env.example             # Environment template
├── requirements.txt         # Dependencies
├── pytest.ini               # Test configuration
└── README.md                # This file
```

## Security

- All endpoints require JWT authentication
- User data is isolated by user_id
- Database queries are scoped to authenticated user
- CORS configured for specific frontend origin
- No hardcoded secrets

## Error Responses

All errors return consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

## HTTP Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (delete)
- `400` - Bad Request
- `401` - Unauthorized (invalid/missing token)
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error

## Development

### Adding New Endpoints

1. Add CRUD function in `app/crud.py`
2. Add route in `app/routers/todos.py`
3. Add tests in `tests/`

### Database Migrations

The database schema is created automatically on startup using SQLModel's `create_all()`.

For production, consider using Alembic for migrations.

## Troubleshooting

**JWT Secret Mismatch:**
- Ensure `JWT_SECRET_KEY` matches frontend `BETTER_AUTH_SECRET`

**Database Connection Errors:**
- Verify `DATABASE_URL` is correct
- Ensure `?sslmode=require` is included for Neon
- Check database is not paused in Neon console

**CORS Errors:**
- Verify `FRONTEND_URL` matches your frontend URL exactly
- No trailing slash in URL

## License

MIT
