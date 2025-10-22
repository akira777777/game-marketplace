"""
Authentication utilities and JWT handling
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..models import User
from ..schemas import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    """Verify JWT token and return token data"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        exp: int = payload.get("exp")
        token_type_payload: str = payload.get("type")

        if username is None or user_id is None:
            return None

        if token_type_payload != token_type:
            return None

        # Check if token is expired
        if exp and datetime.utcnow().timestamp() > exp:
            return None

        return TokenData(user_id=user_id, username=username)

    except JWTError:
        return None


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user by username and password"""
    user = (
        db.query(User)
        .filter((User.username == username) | (User.email == username))
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )
    return current_user


def get_current_seller(current_user: User = Depends(get_current_user)) -> User:
    """Get current user with seller privileges"""
    if current_user.role not in ["seller", "moderator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Seller privileges required"
        )
    return current_user


def get_current_moderator(current_user: User = Depends(get_current_user)) -> User:
    """Get current user with moderator privileges"""
    if current_user.role not in ["moderator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator privileges required",
        )
    return current_user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Get current user with admin privileges"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user


# Optional user dependency (for public endpoints that can show more info if logged in)
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None

    try:
        token = credentials.credentials
        token_data = verify_token(token)
        if token_data is None:
            return None

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user is None or not user.is_active:
            return None

        return user
    except:
        return None
