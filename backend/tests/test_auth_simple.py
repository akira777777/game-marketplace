"""Simple authentication tests without complex password hashing."""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import User
from app.core.auth import create_access_token


def test_simple_user_creation(db_session: Session):
    """Test creating user with simple mock password."""
    # Создаем пользователя с простым mock паролем
    user = User(
        username="simple_test_user",
        email="simple@test.com",
        hashed_password="mock_hash_password_for_testing",
        display_name="Simple Test User",
        is_active=True,
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Проверяем что пользователь создался
    assert user.id is not None
    assert user.username == "simple_test_user"
    assert user.email == "simple@test.com"
    assert user.is_active is True


def test_token_creation():
    """Test JWT token creation."""
    # Создаем токен
    token_data = {"sub": "testuser", "user_id": 1}
    token = create_access_token(data=token_data)
    
    # Проверяем что токен создался
    assert isinstance(token, str)
    assert len(token) > 20
    # JWT токен имеет 3 части разделенные точками
    assert len(token.split(".")) == 3


def test_database_operations(db_session: Session):
    """Test basic database operations."""
    # Проверяем что можем выполнять SQL запросы
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1
    
    # Проверяем что таблицы существуют
    tables = db_session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    ).fetchall()
    
    table_names = [table[0] for table in tables]
    assert "users" in table_names
    assert "games" in table_names
    assert "lots" in table_names


def test_user_persistence(db_session: Session):
    """Test user data persistence across operations."""
    # Создаем пользователя
    user = User(
        username="persist_user",
        email="persist@test.com",
        hashed_password="mock_hash",
        is_active=True,
    )
    
    db_session.add(user)
    db_session.commit()
    user_id = user.id
    
    # Закрываем сессию и открываем новую
    db_session.expunge(user)
    
    # Находим пользователя в БД
    found_user = db_session.query(User).filter(User.id == user_id).first()
    
    assert found_user is not None
    assert found_user.username == "persist_user"
    assert found_user.email == "persist@test.com"


@pytest.mark.integration
def test_auth_headers_format():
    """Test authentication headers format."""
    # Тестируем формат заголовков авторизации
    token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}
    
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")
    
    # Извлекаем токен из заголовка
    extracted_token = headers["Authorization"].split(" ")[1]
    assert extracted_token == token
    assert len(extracted_token.split(".")) == 3