"""
Authentication routes - registration, login, refresh tokens
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_token,
    get_current_user,
)
from ..schemas import UserCreate, UserResponse, Token, TokenRefresh, UserLogin, Message
from ..models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register new user"""

    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        display_name=user_data.display_name,
        phone=user_data.phone,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    """Login user and return access token"""

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 60 * 60,  # 1 hour in seconds
    }


@router.post("/login/json", response_model=Token)
def login_user_json(user_credentials: UserLogin, db: Session = Depends(get_db)) -> Any:
    """Login user with JSON payload"""

    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 60 * 60,
    }


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    token_data: TokenRefresh, db: Session = Depends(get_db)
) -> Any:
    """Refresh access token using refresh token"""

    # Verify refresh token
    token_payload = verify_token(token_data.refresh_token, token_type="refresh")
    if not token_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    # Get user
    user = db.query(User).filter(User.id == token_payload.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new tokens
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    new_refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": 60 * 60,
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> Any:
    """Get current user information"""
    return current_user


@router.post("/logout", response_model=Message)
def logout_user(current_user: User = Depends(get_current_user)) -> Any:
    """Logout user (client should delete tokens)"""
    # In a production app, you might want to blacklist the tokens
    # For now, we just return a success message
    return {"message": "Successfully logged out"}


@router.post("/verify-token", response_model=Message)
def verify_token_endpoint(current_user: User = Depends(get_current_user)) -> Any:
    """Verify if current token is valid"""
    return {"message": "Token is valid"}
