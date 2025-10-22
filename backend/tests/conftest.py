"""Test configuration and fixtures for pytest."""

import os
import sys
import tempfile
from typing import Generator, Dict, Any
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from pytest import MonkeyPatch

# Добавляем путь к модулю app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402
from app.core.database import Base, get_db  # noqa: E402
from app.core.auth import create_access_token, get_password_hash  # noqa: E402
from app.models import User, Game, Lot, Category  # noqa: E402


# Test database configuration - используем in-memory SQLite для тестов
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
    echo=False,  # Отключаем логирование SQL для тестов
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(scope="session")
def test_db() -> Generator[Session, None, None]:
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database once per session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create clean database session for each test with transaction rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    
    # Bind session to connection
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create test client with database dependency override."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            # Cleanup handled by db_session fixture
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """Test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "display_name": "Test User",
        "bio": "Test user bio",
    }


@pytest.fixture
def test_user(db_session: Session, test_user_data: Dict[str, Any]) -> User:
    """Create test user in database."""
    user = User(
        username=test_user_data["username"],
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        display_name=test_user_data.get("display_name"),
        bio=test_user_data.get("bio"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session: Session) -> User:
    """Create test admin user."""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("AdminPassword123!"),
        display_name="Admin User",
        role="admin",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_auth_headers(test_user: User) -> Dict[str, str]:
    """Create authentication headers for test user."""
    access_token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_admin_headers(test_admin_user: User) -> Dict[str, str]:
    """Create authentication headers for admin user."""
    access_token = create_access_token(data={"sub": test_admin_user.username})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_game_data() -> Dict[str, Any]:
    """Test game data."""
    from datetime import date
    return {
        "name": "Test Game",
        "slug": "test-game",
        "description": "A test game for testing purposes",
        "developer": "Test Developer",
        "publisher": "Test Publisher",
        "release_date": date(2023, 1, 1),
        "is_active": True,
    }


@pytest.fixture
def test_game(db_session: Session, test_game_data: Dict[str, Any]) -> Game:
    """Create test game in database."""
    game = Game(**test_game_data)
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game


@pytest.fixture
def test_category_data() -> Dict[str, Any]:
    """Test category data."""
    return {
        "name": "Test Category",
        "description": "A test category",
        "is_active": True,
    }


@pytest.fixture
def test_category(
    db_session: Session, test_game: Game, test_category_data: Dict[str, Any]
) -> Category:
    """Create test category in database."""
    category = Category(game_id=test_game.id, **test_category_data)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_lot_data() -> Dict[str, Any]:
    """Test lot data."""
    return {
        "title": "Test Lot",
        "description": "A test lot for testing",
        "price": 29.99,
        "quantity": 1,
        "is_active": True,
    }


@pytest.fixture
def test_lot(
    db_session: Session,
    test_user: User,
    test_game: Game,
    test_category: Category,
    test_lot_data: Dict[str, Any],
) -> Lot:
    """Create test lot in database."""
    lot = Lot(
        seller_id=test_user.id,
        game_id=test_game.id,
        category_id=test_category.id,
        **test_lot_data,
    )
    db_session.add(lot)
    db_session.commit()
    db_session.refresh(lot)
    return lot


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create temporary file for testing file uploads."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(b"fake image data")
        temp_path = tmp.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture(autouse=True)
def mock_external_services(monkeypatch: MonkeyPatch) -> None:
    """Mock external services for testing."""

    # Mock email service (если существует)
    def mock_send_email(*args: Any, **kwargs: Any) -> Dict[str, str]:
        return {"status": "sent", "message_id": "test_123"}

    # Mock file storage service (если существует)
    def mock_upload_file(*args: Any, **kwargs: Any) -> str:
        return "http://example.com/test-image.jpg"

    # Mock payment service (если существует)
    def mock_process_payment(*args: Any, **kwargs: Any) -> Dict[str, str]:
        return {"status": "success", "transaction_id": "test_123"}

    # Применяем моки только если модули существуют
    try:
        monkeypatch.setattr("app.services.email.send_email", mock_send_email)
    except (ImportError, AttributeError):
        pass

    try:
        monkeypatch.setattr(
            "app.services.storage.upload_file", mock_upload_file
        )
    except (ImportError, AttributeError):
        pass

    try:
        monkeypatch.setattr(
            "app.services.payments.process_payment", mock_process_payment
        )
    except (ImportError, AttributeError):
        pass


# Test markers
pytestmark = [
    pytest.mark.asyncio,
]


# Custom test decorators
def integration_test(func):
    """Mark test as integration test."""
    return pytest.mark.integration(func)


def slow_test(func):
    """Mark test as slow test."""
    return pytest.mark.slow(func)


def unit_test(func):
    """Mark test as unit test."""
    return pytest.mark.unit(func)


def api_test(func):
    """Mark test as API test."""
    return pytest.mark.api(func)


def auth_test(func):
    """Mark test as authentication test."""
    return pytest.mark.auth(func)
