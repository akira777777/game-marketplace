"""
Orders management routes
"""

from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from ..core.database import get_db
from ..core.auth import get_current_user, get_current_moderator
from ..schemas import (
    OrderResponse,
    OrderCreate,
    OrderUpdate,
    PaginatedResponse,
    Message,
)
from ..models import Order, Lot, User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=PaginatedResponse[OrderResponse])
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    buyer_id: Optional[int] = Query(None),
    seller_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get orders (user sees only their own orders, moderators see all)"""

    query = db.query(Order).options(
        joinedload(Order.lot).joinedload(Lot.game),
        joinedload(Order.buyer),
        joinedload(Order.seller),
    )

    # Filter by user permissions
    if current_user.role not in ["moderator", "admin"]:
        # Regular users can only see their own orders
        query = query.filter(
            or_(Order.buyer_id == current_user.id, Order.seller_id == current_user.id)
        )
    else:
        # Moderators can filter by buyer/seller
        if buyer_id:
            query = query.filter(Order.buyer_id == buyer_id)
        if seller_id:
            query = query.filter(Order.seller_id == seller_id)

    # Apply status filter
    if status:
        query = query.filter(Order.status == status)

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    return {"items": orders, "total": total, "skip": skip, "limit": limit}


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get order by ID"""

    order = (
        db.query(Order)
        .options(
            joinedload(Order.lot).joinedload(Lot.game),
            joinedload(Order.buyer),
            joinedload(Order.seller),
        )
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check permissions
    if (
        current_user.role not in ["moderator", "admin"]
        and order.buyer_id != current_user.id
        and order.seller_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create new order"""

    # Check if lot exists and is active
    lot = db.query(Lot).filter(Lot.id == order_data.lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lot not found"
        )

    if lot.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lot is not available for purchase",
        )

    # Check if user is not trying to buy their own lot
    if lot.seller_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot buy your own lot"
        )

    # Check if quantity is valid
    if order_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be positive"
        )

    if lot.quantity is not None and order_data.quantity > lot.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough quantity available",
        )

    # Calculate total price
    total_price = lot.price * order_data.quantity

    # Create order
    db_order = Order(
        lot_id=order_data.lot_id,
        buyer_id=current_user.id,
        seller_id=lot.seller_id,
        quantity=order_data.quantity,
        unit_price=lot.price,
        total_price=total_price,
        buyer_message=order_data.buyer_message,
    )

    db.add(db_order)

    # Update lot quantity if applicable
    if lot.quantity is not None:
        lot.quantity -= order_data.quantity
        if lot.quantity == 0:
            lot.status = "sold_out"

    db.commit()
    db.refresh(db_order)

    return db_order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update order status"""

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check permissions
    is_buyer = order.buyer_id == current_user.id
    is_seller = order.seller_id == current_user.id
    is_moderator = current_user.role in ["moderator", "admin"]

    if not (is_buyer or is_seller or is_moderator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Update fields based on permissions
    update_data = order_update.dict(exclude_unset=True)

    # Status transitions validation
    if "status" in update_data:
        new_status = update_data["status"]
        current_status = order.status

        # Define allowed transitions
        allowed_transitions = {
            "pending": (
                ["confirmed", "cancelled"]
                if is_seller or is_moderator
                else ["cancelled"]
            ),
            "confirmed": ["in_progress"] if is_seller or is_moderator else [],
            "in_progress": ["in_escrow"] if is_seller or is_moderator else [],
            "in_escrow": (
                ["completed", "disputed"] if is_buyer or is_moderator else ["disputed"]
            ),
            "disputed": ["completed", "cancelled"] if is_moderator else [],
            "completed": [],
            "cancelled": [],
        }

        if new_status not in allowed_transitions.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status} to {new_status}",
            )

    # Only moderators can update certain fields
    if not is_moderator:
        update_data.pop("buyer_id", None)
        update_data.pop("seller_id", None)
        update_data.pop("lot_id", None)
        update_data.pop("quantity", None)
        update_data.pop("unit_price", None)
        update_data.pop("total_price", None)

    # Only buyer can update buyer_message initially
    if "buyer_message" in update_data and not is_buyer and current_status == "pending":
        update_data.pop("buyer_message")

    # Only seller can update seller_message
    if "seller_message" in update_data and not is_seller and not is_moderator:
        update_data.pop("seller_message")

    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    return order


@router.post("/{order_id}/confirm", response_model=Message)
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Confirm order (seller only)"""

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check permissions
    if order.seller_id != current_user.id and current_user.role not in [
        "moderator",
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only confirm pending orders",
        )

    order.status = "confirmed"
    db.commit()

    return {"message": "Order confirmed successfully"}


@router.post("/{order_id}/cancel", response_model=Message)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Cancel order"""

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check permissions
    is_buyer = order.buyer_id == current_user.id
    is_seller = order.seller_id == current_user.id
    is_moderator = current_user.role in ["moderator", "admin"]

    if not (is_buyer or is_seller or is_moderator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Check if order can be cancelled
    if order.status not in ["pending", "confirmed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled at this stage",
        )

    # Restore lot quantity if order is cancelled
    lot = db.query(Lot).filter(Lot.id == order.lot_id).first()
    if lot and lot.quantity is not None:
        lot.quantity += order.quantity
        if lot.status == "sold_out":
            lot.status = "active"

    order.status = "cancelled"
    db.commit()

    return {"message": "Order cancelled successfully"}


@router.post("/{order_id}/dispute", response_model=Message)
def create_dispute(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create dispute for order (buyer only)"""

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check permissions
    if order.buyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyer can create dispute",
        )

    if order.status != "in_escrow":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only dispute orders in escrow",
        )

    order.status = "disputed"
    db.commit()

    return {"message": "Dispute created successfully"}
