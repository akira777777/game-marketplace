"""Alternative password hashing for testing to avoid bcrypt issues."""

import hashlib
from app.core.auth import get_password_hash


def get_simple_password_hash(password: str) -> str:
    """Simple hash for testing - avoids bcrypt initialization issues."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_simple_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password with simple hash."""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


# Mock auth functions for tests
def mock_password_hash(password: str) -> str:
    """Mock password hash that avoids bcrypt issues."""
    return f"mock_hash_{password}"


def mock_verify_password(plain_password: str, hashed_password: str) -> bool:
    """Mock verify password."""
    return f"mock_hash_{plain_password}" == hashed_password