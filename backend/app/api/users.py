"""
User management routes
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..core.database import get_db
from ..core.auth import (
    get_current_user,
    get_current_admin,
    get_current_moderator,
    get_password_hash,
)
from ..schemas import UserResponse, UserUpdate, UserCreate, PaginatedResponse, Message
from ..models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Get all users (moderator/admin only)"""

    query = db.query(User)

    # Apply filters
    if search:
        query = query.filter(
            or_(
                User.username.contains(search),
                User.email.contains(search),
                User.full_name.contains(search),
            )
        )

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # Get total count
    total = query.count()

    # Apply pagination
    users = query.offset(skip).limit(limit).all()

    return {"items": users, "total": total, "skip": skip, "limit": limit}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get user by ID"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Users can view their own profile, moderators can view any profile
    if user_id != current_user.id and current_user.role not in ["moderator", "admin"]:
        # Return limited public info for other users
        return UserResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            avatar_url=user.avatar_url,
            rating=user.rating,
            reviews_count=user.reviews_count,
            created_at=user.created_at,
            last_seen=user.last_seen,
            is_verified=user.is_verified,
            role=user.role,
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update user"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Users can only update their own profile, admins can update any profile
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Update fields
    update_data = user_update.dict(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Only admins can change role and verification status
    if current_user.role != "admin":
        update_data.pop("role", None)
        update_data.pop("is_verified", None)
        update_data.pop("is_active", None)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", response_model=Message)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> Any:
    """Delete user (admin only)"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Don't allow deleting admin users
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete admin user"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.post("/{user_id}/ban", response_model=Message)
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Ban user (moderator/admin only)"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Don't allow banning admins or moderators
    if user.role in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot ban admin or moderator user",
        )

    user.is_active = False
    db.commit()

    return {"message": f"User {user.username} has been banned"}


@router.post("/{user_id}/unban", response_model=Message)
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Unban user (moderator/admin only)"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.is_active = True
    db.commit()

    return {"message": f"User {user.username} has been unbanned"}


@router.post("/{user_id}/verify", response_model=Message)
def verify_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Verify user (moderator/admin only)"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.is_verified = True
    db.commit()

    return {"message": f"User {user.username} has been verified"}


@router.post("/upload-avatar", response_model=Message)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Upload user avatar"""

    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image"
        )

    # Check file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB",
        )

    # In a real app, you would save the file to cloud storage
    # For now, we'll just simulate updating the avatar URL
    avatar_url = f"/static/avatars/{current_user.id}_{file.filename}"

    current_user.avatar_url = avatar_url
    db.commit()

    return {"message": "Avatar uploaded successfully"}
