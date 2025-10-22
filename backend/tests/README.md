# Test configuration for the GameMarketplace backend

# Pytest configuration
# Run tests: pytest
# Run with coverage: pytest --cov=app --cov-report=html
# Run specific markers: pytest -m unit  or  pytest -m integration

# Test database
# Uses in-memory SQLite for fast test execution
# Each test gets a clean database session with transaction rollback

# Test structure:
# - conftest.py: Main test configuration and fixtures
# - test_*.py: Individual test modules
# - Use markers to organize tests: @unit_test, @integration_test, etc.

# Available fixtures:
# - db_session: Clean database session for each test
# - client: FastAPI test client with dependency overrides
# - test_user: Test user with authentication
# - test_admin_user: Test admin user
# - test_game, test_category, test_lot: Test models
# - test_auth_headers, test_admin_headers: Authentication headers
# - temp_file: Temporary file for upload tests

# External services are mocked by default in conftest.py