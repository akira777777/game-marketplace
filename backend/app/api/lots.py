"""
Lots (trading offers) management routes
"""

from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_

from ..core.database import get_db
from ..core.auth import (
    get_current_user,
    get_current_seller,
    get_current_moderator,
    get_current_user_optional,
)
from ..schemas import LotResponse, LotCreate, LotUpdate, PaginatedResponse, Message
from ..models import Lot, LotStatus, Game, User, Order

router = APIRouter(prefix="/lots", tags=["Lots"])


@router.get("/", response_model=PaginatedResponse[LotResponse])
def get_lots(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    game_id: Optional[int] = Query(None),
    seller_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    status: Optional[str] = Query("active"),
    sort_by: str = Query("created_at", regex="^(created_at|price|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Any:
    """Get all lots with filters"""

    query = db.query(Lot)  # Убираем joinedload для тестирования

    # Apply filters
    if search:
        query = query.filter(
            or_(Lot.title.contains(search), Lot.description.contains(search))
        )

    if game_id:
        query = query.filter(Lot.game_id == game_id)

    if seller_id:
        query = query.filter(Lot.seller_id == seller_id)

    if min_price is not None:
        query = query.filter(Lot.price >= min_price)

    if max_price is not None:
        query = query.filter(Lot.price <= max_price)

    # Only show active lots to regular users
    if not current_user or current_user.role not in ["moderator", "admin"]:
        query = query.filter(Lot.status == LotStatus.ACTIVE)
    elif status:
        # Convert string status to enum for comparison
        if status == "active":
            query = query.filter(Lot.status == LotStatus.ACTIVE)
        elif status == "sold":
            query = query.filter(Lot.status == LotStatus.SOLD)
        elif status == "inactive":
            query = query.filter(Lot.status == LotStatus.INACTIVE)
        elif status == "moderation":
            query = query.filter(Lot.status == LotStatus.MODERATION)

    # Apply sorting
    if sort_by == "created_at":
        order_column = Lot.created_at
    elif sort_by == "price":
        order_column = Lot.price
    elif sort_by == "title":
        order_column = Lot.title
    else:
        order_column = Lot.created_at

    if sort_order == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    # Get total count
    total = query.count()

    # Apply pagination
    lots = query.offset(skip).limit(limit).all()

    return {"items": lots, "total": total, "skip": skip, "limit": limit}


@router.get("/{lot_id}", response_model=LotResponse)
def get_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Any:
    """Get lot by ID"""

    lot = (
        db.query(Lot)
        .options(joinedload(Lot.game), joinedload(Lot.seller))
        .filter(Lot.id == lot_id)
        .first()
    )

    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Only show active lots to regular users
    if (
        not current_user or current_user.role not in ["moderator", "admin"]
    ) and lot.status != "active":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Increment views count (only for active lots and not for the seller)
    if lot.status == "active" and (
        not current_user or current_user.id != lot.seller_id
    ):
        lot.views += 1
        db.commit()

    return lot


@router.post("/", response_model=LotResponse, status_code=status.HTTP_201_CREATED)
def create_lot(
    lot_data: LotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_seller),
) -> Any:
    """Create new lot (seller+ only)"""

    # Check if game exists
    game = db.query(Game).filter(Game.id == lot_data.game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Game not found"
        )

    # Check if game is active
    if not game.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create lot for inactive game",
        )

    # Create lot
    db_lot = Lot(**lot_data.dict(), seller_id=current_user.id)

    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)

    return db_lot


@router.put("/{lot_id}", response_model=LotResponse)
def update_lot(
    lot_id: int,
    lot_update: LotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update lot"""

    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Only seller or moderator/admin can update lot
    if lot.seller_id != current_user.id and current_user.role not in [
        "moderator",
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Update fields
    update_data = lot_update.dict(exclude_unset=True)

    # Check if game exists if being updated
    if "game_id" in update_data:
        game = db.query(Game).filter(Game.id == update_data["game_id"]).first()
        if not game or not game.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game not found or inactive",
            )

    # Only moderators can change status directly
    if "status" in update_data and current_user.role not in ["moderator", "admin"]:
        if lot.seller_id == current_user.id:
            # Sellers can only deactivate their own lots
            if update_data["status"] not in ["inactive", "active"]:
                update_data.pop("status")
        else:
            update_data.pop("status")

    for field, value in update_data.items():
        setattr(lot, field, value)

    db.commit()
    db.refresh(lot)

    return lot


@router.delete("/{lot_id}", response_model=Message)
def delete_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Delete lot"""

    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Only seller or moderator/admin can delete lot
    if lot.seller_id != current_user.id and current_user.role not in [
        "moderator",
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Check if lot has active orders
    active_orders = (
        db.query(Order)
        .filter(
            and_(
                Order.lot_id == lot_id,
                Order.status.in_(["pending", "in_progress", "in_escrow"]),
            )
        )
        .first()
    )

    if active_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete lot with active orders",
        )

    db.delete(lot)
    db.commit()

    return {"message": "Lot deleted successfully"}


@router.post("/{lot_id}/deactivate", response_model=Message)
def deactivate_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Deactivate lot"""

    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Only seller or moderator/admin can deactivate lot
    if lot.seller_id != current_user.id and current_user.role not in [
        "moderator",
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    lot.status = "inactive"
    db.commit()

    return {"message": "Lot deactivated successfully"}


@router.post("/{lot_id}/activate", response_model=Message)
def activate_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Activate lot"""

    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found"
        )

    # Only seller or moderator/admin can activate lot
    if lot.seller_id != current_user.id and current_user.role not in [
        "moderator",
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Check if game is still active
    game = db.query(Game).filter(Game.id == lot.game_id).first()
    if not game or not game.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot activate lot for inactive game",
        )

    lot.status = "active"
    db.commit()

    return {"message": "Lot activated successfully"}


@router.get("/user/{user_id}", response_model=PaginatedResponse[LotResponse])
def get_user_lots(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Any:
    """Get lots by user"""

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    query = db.query(Lot).options(joinedload(Lot.game)).filter(Lot.seller_id == user_id)

    # Only show active lots to other users
    if not current_user or (
        current_user.id != user_id and current_user.role not in ["moderator", "admin"]
    ):
        query = query.filter(Lot.status == "active")
    elif status:
        query = query.filter(Lot.status == status)

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    lots = query.order_by(Lot.created_at.desc()).offset(skip).limit(limit).all()

    return {"items": lots, "total": total, "skip": skip, "limit": limit}
