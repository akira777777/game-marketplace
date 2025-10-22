# Code Style and Conventions

## Python/Backend Conventions

### Code Formatting
- **Black** for code formatting (available in requirements)
- **isort** for import sorting
- **flake8** for linting
- Line length: 88 characters (Black default)

### Naming Conventions
- **Classes**: PascalCase (e.g., `User`, `GameCategory`)
- **Functions/Variables**: snake_case (e.g., `get_user`, `user_id`)
- **Constants**: UPPER_CASE (e.g., `SECRET_KEY`, `MAX_FILE_SIZE`)
- **Files/Modules**: snake_case (e.g., `user_service.py`)

### Type Hints
- Required for all function parameters and return types
- Use modern Python typing (from `typing` module)
- Example: `def get_user(user_id: int) -> Optional[User]:`

### Documentation
- Docstrings for all classes and functions
- Use triple quotes for docstrings
- Example format:
```python
def create_user(username: str, email: str) -> User:
    """Create a new user account.
    
    Args:
        username: Unique username for the account
        email: User's email address
        
    Returns:
        Created user object
        
    Raises:
        ValueError: If username already exists
    """
```

### Database Models
- Use SQLAlchemy declarative base
- Relationships should be explicit and bidirectional
- Include appropriate indexes for queries
- Use enums for status fields

### API Design
- RESTful URL patterns
- Consistent response formats
- Proper HTTP status codes
- Request/response validation with Pydantic

## File Organization
- Keep related functionality together
- Separate models, services, and API layers
- Use dependency injection for database sessions
- Configuration should be centralized in core/config.py