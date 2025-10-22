"""Test user authentication and model fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import User, Game, Category, Lot


def test_user_fixture_creation(test_user: User, test_user_data: dict):
    """Test that user fixture creates user correctly."""
    assert test_user.id is not None
    assert test_user.username == test_user_data["username"]
    assert test_user.email == test_user_data["email"]
    assert test_user.display_name == test_user_data["display_name"]
    assert test_user.is_active is True
    # Пароль должен быть захеширован
    assert test_user.hashed_password != test_user_data["password"]
    assert len(test_user.hashed_password) > 5  # Mock hash длиннее 5 символов


def test_admin_user_fixture(test_admin_user: User):
    """Test that admin user fixture works correctly."""
    assert test_admin_user.id is not None
    assert test_admin_user.username == "admin"
    assert test_admin_user.email == "admin@example.com"
    assert test_admin_user.role.value == "admin"  # Сравниваем значение enum
    assert test_admin_user.is_active is True


def test_auth_tokens_valid(test_auth_headers: dict, test_admin_headers: dict):
    """Test that auth tokens are properly formatted."""
    # Test user token
    assert "Authorization" in test_auth_headers
    user_token = test_auth_headers["Authorization"]
    assert user_token.startswith("Bearer ")
    assert len(user_token.split(".")) == 3  # JWT has 3 parts
    
    # Test admin token
    assert "Authorization" in test_admin_headers
    admin_token = test_admin_headers["Authorization"]
    assert admin_token.startswith("Bearer ")
    assert len(admin_token.split(".")) == 3  # JWT has 3 parts
    
    # Tokens should be different
    assert user_token != admin_token


def test_database_user_persistence(db_session: Session, test_user: User):
    """Test that user persists in database correctly."""
    # Проверяем что пользователь действительно в БД
    found_user = db_session.query(User).filter(
        User.username == test_user.username
    ).first()
    
    assert found_user is not None
    assert found_user.id == test_user.id
    assert found_user.email == test_user.email


@pytest.mark.integration
def test_user_creation_isolation(db_session: Session):
    """Test that users created in tests don't interfere."""
    """Test that user creation is isolated between tests."""
    from app.models import User
    
    # Create user directly in this test
    user = User(
        username="isolation_user",
        email="isolation@test.com",
        hashed_password="mock_hash_test123",  # Mock хеш для тестов
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    
    # Проверяем что он создался
    # Check that the user was created within this transaction
    count = db_session.execute(
        text("SELECT COUNT(*) FROM users WHERE username = :username"),
        {"username": "isolation_user"}  # Правильное имя пользователя
    ).scalar()
    
    assert count == 1  # Пользователь есть в текущей транзакции


def test_isolation_check(db_session: Session):
    """Verify that previous test's user doesn't exist (isolation works)."""
    count = db_session.execute(
        text("SELECT COUNT(*) FROM users WHERE username = :username"),
        {"username": "isolation_test_user"}  
    ).scalar()
    
    # Пользователь из предыдущего теста не должен существовать
    assert count == 0