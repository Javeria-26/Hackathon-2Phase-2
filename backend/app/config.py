from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_HOURS: int = 24

    # Database Configuration
    DATABASE_URL: str

    # CORS Configuration
    FRONTEND_URL: str = "http://localhost:3000"

    # Application Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
