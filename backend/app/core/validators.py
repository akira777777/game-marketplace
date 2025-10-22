"""Enhanced validation utilities using Pydantic v2."""

import re
from typing import Any, Dict, List, Optional, Union
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ValidationError(Exception):
    """Custom validation error."""

    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"Validation error in '{field}': {message}")


class BaseValidator(BaseModel):
    """Base validator with common configuration."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
        use_enum_values=True,
    )


class UserValidators:
    """Validation helpers for user-related data."""

    @staticmethod
    def validate_username(value: str) -> str:
        """Validate username format."""
        if not value:
            raise ValidationError("username", "Username cannot be empty")

        if len(value) < 3:
            raise ValidationError("username", "Username must be at least 3 characters")

        if len(value) > 50:
            raise ValidationError(
                "username", "Username must be less than 50 characters"
            )

        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise ValidationError(
                "username",
                "Username can only contain letters, numbers, underscores, and hyphens",
            )

        return value

    @staticmethod
    def validate_email(value: str) -> str:
        """Validate email format."""
        try:
            validated_email = validate_email(value)
            return validated_email.email
        except EmailNotValidError as e:
            raise ValidationError("email", str(e))

    @staticmethod
    def validate_password(value: str) -> str:
        """Validate password strength."""
        if not value:
            raise ValidationError("password", "Password cannot be empty")

        if len(value) < 8:
            raise ValidationError("password", "Password must be at least 8 characters")

        if len(value) > 128:
            raise ValidationError(
                "password", "Password must be less than 128 characters"
            )

        # Check for at least one digit
        if not re.search(r"\d", value):
            raise ValidationError(
                "password", "Password must contain at least one digit"
            )

        # Check for at least one letter
        if not re.search(r"[a-zA-Z]", value):
            raise ValidationError(
                "password", "Password must contain at least one letter"
            )

        return value


class FileValidators:
    """Validation helpers for file uploads."""

    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate_image_file(filename: str, file_size: int) -> str:
        """Validate image file."""
        if not filename:
            raise ValidationError("filename", "Filename cannot be empty")

        # Check extension
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        if f".{ext}" not in FileValidators.ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(
                "filename",
                f"Invalid file type. Allowed: {', '.join(FileValidators.ALLOWED_IMAGE_EXTENSIONS)}",
            )

        # Check file size
        if file_size > FileValidators.MAX_IMAGE_SIZE:
            raise ValidationError(
                "file_size",
                f"File too large. Maximum size: {FileValidators.MAX_IMAGE_SIZE // (1024*1024)}MB",
            )

        return filename


class GameValidators:
    """Validation helpers for game-related data."""

    @staticmethod
    def validate_price(value: Union[int, float]) -> float:
        """Validate price value."""
        if value < 0:
            raise ValidationError("price", "Price cannot be negative")

        if value > 999999.99:
            raise ValidationError("price", "Price cannot exceed 999,999.99")

        # Round to 2 decimal places
        return round(float(value), 2)

    @staticmethod
    def validate_game_name(value: str) -> str:
        """Validate game name."""
        if not value:
            raise ValidationError("name", "Game name cannot be empty")

        if len(value) < 2:
            raise ValidationError("name", "Game name must be at least 2 characters")

        if len(value) > 100:
            raise ValidationError("name", "Game name must be less than 100 characters")

        return value


class PaginationValidators:
    """Validation helpers for pagination."""

    @staticmethod
    def validate_page(value: int) -> int:
        """Validate page number."""
        if value < 1:
            raise ValidationError("page", "Page number must be at least 1")

        if value > 10000:
            raise ValidationError("page", "Page number cannot exceed 10,000")

        return value

    @staticmethod
    def validate_limit(value: int) -> int:
        """Validate page limit."""
        if value < 1:
            raise ValidationError("limit", "Limit must be at least 1")

        if value > 100:
            raise ValidationError("limit", "Limit cannot exceed 100")

        return value


# Enhanced schemas with validation
class UserCreateSchema(BaseValidator):
    """Schema for user creation."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return UserValidators.validate_username(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return UserValidators.validate_email(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return UserValidators.validate_password(v)


class GameCreateSchema(BaseValidator):
    """Schema for game creation."""

    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[float] = Field(None, ge=0, le=999999.99)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return GameValidators.validate_game_name(v)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            return GameValidators.validate_price(v)
        return v


class PaginationSchema(BaseValidator):
    """Schema for pagination parameters."""

    page: int = Field(default=1, ge=1, le=10000)
    limit: int = Field(default=20, ge=1, le=100)

    @field_validator("page")
    @classmethod
    def validate_page(cls, v: int) -> int:
        return PaginationValidators.validate_page(v)

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: int) -> int:
        return PaginationValidators.validate_limit(v)
