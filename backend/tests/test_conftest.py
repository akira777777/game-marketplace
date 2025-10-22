"""Test conftest fixtures and basic functionality."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, Game, Category, Lot


def test_db_session_fixture(db_session: Session):
    """Test database session fixture works."""
    from sqlalchemy import text
    
    assert db_session is not None
    # Test that we can execute a simple query
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1


def test_client_fixture(client: TestClient):
    """Test FastAPI client fixture works."""
    assert client is not None
    # Test that we can make a request
    response = client.get("/")
    # Should return 200 or at least not crash
    assert response.status_code in [200, 404, 422]


def test_user_fixtures(
    test_user: User, 
    test_admin_user: User, 
    test_user_data: dict
):
    """Test user fixtures work correctly."""
    # Test regular user
    assert test_user.username == test_user_data["username"]
    assert test_user.email == test_user_data["email"]
    assert test_user.is_active is True
    
    # Test admin user
    assert test_admin_user.username == "admin"
    assert test_admin_user.role.value == "admin"  # Сравниваем значение enum
    assert test_admin_user.is_active is True


def test_auth_headers_fixtures(test_auth_headers, test_admin_headers):
    """Test authentication header fixtures."""
    # Test user headers
    assert "Authorization" in test_auth_headers
    assert test_auth_headers["Authorization"].startswith("Bearer ")
    
    # Test admin headers
    assert "Authorization" in test_admin_headers
    assert test_admin_headers["Authorization"].startswith("Bearer ")


def test_game_fixture(test_game: Game, test_game_data: dict):
    """Test game fixture works correctly."""
    assert test_game.name == test_game_data["name"]
    assert test_game.developer == test_game_data["developer"]
    assert test_game.is_active is True


def test_category_fixture(test_category: Category, test_game: Game):
    """Test category fixture works correctly."""
    assert test_category.name == "Test Category"
    assert test_category.game_id == test_game.id
    assert test_category.is_active is True


def test_lot_fixture(
    test_lot: Lot, 
    test_user: User, 
    test_game: Game, 
    test_category: Category
):
    """Test lot fixture works correctly."""
    assert test_lot.title == "Test Lot"
    assert test_lot.seller_id == test_user.id
    assert test_lot.game_id == test_game.id
    assert test_lot.category_id == test_category.id
    assert test_lot.price == 29.99


def test_temp_file_fixture(temp_file):
    """Test temporary file fixture."""
    import os
    
    assert os.path.exists(temp_file)
    assert temp_file.endswith('.jpg')
    
    # Verify file has content
    with open(temp_file, 'rb') as f:
        content = f.read()
        assert len(content) > 0


@pytest.mark.integration  
def test_database_isolation(db_session: Session):
    """Test that database changes are isolated between tests."""
    # Add a user to the database
    
    user = User(
        username="isolation_test",
        email="isolation@test.com",
        hashed_password="mock_hash_testpass",  # Mock хеш для тестов
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    
    # Verify user exists
    found_user = db_session.query(User).filter(
        User.username == "isolation_test"
    ).first()
    assert found_user is not None
    assert found_user.username == "isolation_test"


def test_database_isolation_check(db_session: Session):
    """Test that previous test's user doesn't exist (isolation works)."""
    # This test should not see the user from the previous test
    found_user = db_session.query(User).filter(
        User.username == "isolation_test"
    ).first()
    assert found_user is None


@pytest.mark.api
def test_api_with_auth(client: TestClient, test_auth_headers):
    """Test API endpoints with authentication."""
    # This is a template for API tests
    # Replace with actual API endpoints when they exist
    
    # Example: Test user profile endpoint
    # response = client.get("/api/v1/users/me", headers=test_auth_headers)
    # assert response.status_code == 200
    
    # For now, just test that headers are properly formatted
    assert "Authorization" in test_auth_headers
    token = test_auth_headers["Authorization"]
    assert token.startswith("Bearer ")
    assert len(token) > 10  # Should have actual token content
