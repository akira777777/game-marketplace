"""
Core application settings and configuration
"""

import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings"""

    # Basic app info
    APP_NAME: str = "GameMarketplace API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("ENVIRONMENT", "development") != "production"

    # Database - PostgreSQL/Neon
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_ECHO: bool = False

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-super-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # Production CORS origins from environment
    CORS_ORIGINS: List[str] = []

    # File upload
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

    # Email (для уведомлений)
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[int] = None
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def database_url_sync(self) -> str:
        """Get sync database URL"""
        url = self.DATABASE_URL
        if not url:
            raise ValueError("DATABASE_URL must be set")
        # Convert postgres:// to postgresql:// for SQLAlchemy 2.0
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    
    @property
    def database_url_async(self) -> str:
        """Get async database URL for PostgreSQL"""
        url = self.DATABASE_URL
        if not url:
            raise ValueError("DATABASE_URL must be set")
        # Convert to asyncpg format
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


# Create settings instance
settings = Settings()
