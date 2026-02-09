from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import create_db_and_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    Runs on startup and shutdown.
    """
    # Startup
    settings = get_settings()

    # Validate JWT_SECRET_KEY is set
    if not settings.JWT_SECRET_KEY or len(settings.JWT_SECRET_KEY) < 32:
        raise ValueError("JWT_SECRET_KEY must be set and at least 32 characters long")

    print("Creating database tables...")
    try:
        await create_db_and_tables()
        print("Application started")
    except Exception as e:
        print(f"Failed to create database tables: {str(e)}")
        raise

    yield

    # Shutdown
    print("Closing database connections...")
    await engine.dispose()
    print("Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Specific origin, not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
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
    """Handle unexpected errors."""
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


# Register routers
from app.routers import todos
app.include_router(todos.router, tags=["todos"])


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Todo API is running"}
