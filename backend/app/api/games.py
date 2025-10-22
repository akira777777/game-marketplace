"""
Games and categories management routes
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..core.database import get_db
from ..core.auth import (
    get_current_user,
    get_current_moderator,
    get_current_user_optional,
)
from ..schemas import (
    GameResponse,
    GameCreate,
    GameUpdate,
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    PaginatedResponse,
    Message,
)
from ..models import Game, Category, User

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/", response_model=PaginatedResponse[GameResponse])
def get_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(True),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Any:
    """Get all games"""

    query = db.query(Game)

    # Apply filters
    if search:
        query = query.filter(
            or_(Game.name.contains(search), Game.description.contains(search))
        )

    if category_id:
        # Filter games that have the specified category
        query = query.join(Game.categories).filter(Category.id == category_id)

    # Only show active games to regular users
    if not current_user or current_user.role not in ["moderator", "admin"]:
        query = query.filter(Game.is_active == True)
    elif is_active is not None:
        query = query.filter(Game.is_active == is_active)

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    games = query.order_by(Game.name).offset(skip).limit(limit).all()

    return {"items": games, "total": total, "skip": skip, "limit": limit}


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Any:
    """Get game by ID"""

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    # Only show active games to regular users
    if (
        not current_user or current_user.role not in ["moderator", "admin"]
    ) and not game.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    return game


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(
    game_data: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Create new game (moderator/admin only)"""

    # Check if game already exists
    existing_game = db.query(Game).filter(Game.name == game_data.name).first()
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this name already exists",
        )

    db_game = Game(**game_data.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    game_update: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Update game (moderator/admin only)"""

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    # Update fields
    update_data = game_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(game, field, value)

    db.commit()
    db.refresh(game)

    return game


@router.delete("/{game_id}", response_model=Message)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Delete game (moderator/admin only)"""

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    db.delete(game)
    db.commit()

    return {"message": "Game deleted successfully"}


# Categories endpoints
categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("/", response_model=List[CategoryResponse])
def get_categories(
    parent_id: Optional[int] = Query(None), db: Session = Depends(get_db)
) -> Any:
    """Get all categories"""

    query = db.query(Category)

    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)
    else:
        # Get root categories by default
        query = query.filter(Category.parent_id.is_(None))

    categories = query.order_by(Category.name).all()
    return categories


@categories_router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)) -> Any:
    """Get category by ID"""

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return category


@categories_router.post(
    "/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Create new category (moderator/admin only)"""

    # Check if parent category exists
    if category_data.parent_id:
        parent = (
            db.query(Category).filter(Category.id == category_data.parent_id).first()
        )
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )

    # Check if category already exists
    existing_category = (
        db.query(Category)
        .filter(
            Category.name == category_data.name,
            Category.parent_id == category_data.parent_id,
        )
        .first()
    )
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    db_category = Category(**category_data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@categories_router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Update category (moderator/admin only)"""

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Update fields
    update_data = category_update.dict(exclude_unset=True)

    # Check if parent category exists if being updated
    if "parent_id" in update_data and update_data["parent_id"]:
        parent = (
            db.query(Category).filter(Category.id == update_data["parent_id"]).first()
        )
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@categories_router.delete("/{category_id}", response_model=Message)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
) -> Any:
    """Delete category (moderator/admin only)"""

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if category has subcategories or games
    subcategories = db.query(Category).filter(Category.parent_id == category_id).first()
    games = db.query(Game).filter(Game.category_id == category_id).first()

    if subcategories or games:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with subcategories or games",
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}


# Include categories router
router.include_router(categories_router)
