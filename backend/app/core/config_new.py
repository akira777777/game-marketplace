"""Enhanced configuration management with environment validation."""

import os
from functools import lru_cache
from typing import List, Optional, Any
from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""

    # Application
    APP_NAME: str = Field(default="GameMarketplace API", env="APP_NAME")
    VERSION: str = Field(default="1.0.0", env="VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    DESCRIPTION: str = Field(
        default="A marketplace for gaming items and services", env="DESCRIPTION"
    )

    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DOCS_URL: Optional[str] = Field(default="/docs", env="DOCS_URL")
    REDOC_URL: Optional[str] = Field(default="/redoc", env="REDOC_URL")

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./gamemp.db", env="DATABASE_URL")

    # Redis
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production", env="SECRET_KEY"
    )
    JWT_SECRET_KEY: str = Field(
        default="your-jwt-secret-key-change-this-in-production", env="JWT_SECRET_KEY"
    )
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # CORS
    CORS_ORIGINS: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    # File Upload
    UPLOAD_DIR: str = Field(default="static", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp"],
        env="ALLOWED_IMAGE_EXTENSIONS",
    )

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")

    # Email Configuration
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")

    # External Services
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, env="STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(
        default=None, env="STRIPE_PUBLISHABLE_KEY"
    )

    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")

    # Testing
    TESTING: bool = Field(default=False, env="TESTING")

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("ALLOWED_IMAGE_EXTENSIONS", pre=True)
    def parse_allowed_extensions(cls, v: Any) -> List[str]:
        """Parse allowed extensions from string or list."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

    @validator("LOG_LEVEL")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {valid_levels}")
        return v.upper()

    @validator("PORT")
    def validate_port(cls, v: int) -> int:
        """Validate port number."""
        if not (1 <= v <= 65535):
            raise ValueError("PORT must be between 1 and 65535")
        return v

    @validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    def validate_token_expire(cls, v: int) -> int:
        """Validate token expiration time."""
        if v <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
        return v

    @validator("MAX_FILE_SIZE")
    def validate_max_file_size(cls, v: int) -> int:
        """Validate max file size."""
        if v <= 0:
            raise ValueError("MAX_FILE_SIZE must be positive")
        if v > 100 * 1024 * 1024:  # 100MB
            raise ValueError("MAX_FILE_SIZE cannot exceed 100MB")
        return v

    @validator("SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secret_keys(cls, v: str, field) -> str:
        """Validate secret keys."""
        if len(v) < 32:
            raise ValueError(f"{field.name} must be at least 32 characters long")
        return v

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.DEBUG and not self.TESTING

    def get_database_url(self) -> str:
        """Get database URL with fallback for testing."""
        if self.TESTING:
            return "sqlite:///./test_gamemp.db"
        return self.DATABASE_URL

    def get_redis_url(self) -> Optional[str]:
        """Get Redis URL if available."""
        return self.REDIS_URL

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
