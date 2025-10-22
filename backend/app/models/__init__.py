"""
Database models for GameMarketplace
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Numeric,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from datetime import datetime
from ..core.database import Base


class OrderStatus(PyEnum):
    """Order status enumeration"""

    PENDING = "pending"
    PAID = "paid"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class LotStatus(PyEnum):
    """Lot status enumeration"""

    ACTIVE = "active"
    SOLD = "sold"
    INACTIVE = "inactive"
    MODERATION = "moderation"


class UserRole(PyEnum):
    """User role enumeration"""

    USER = "user"
    SELLER = "seller"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Profile info
    display_name = Column(String(100))
    avatar_url = Column(String(255))
    bio = Column(Text)

    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

    # Stats
    rating = Column(Numeric(3, 2), default=0.0)
    total_reviews = Column(Integer, default=0)
    total_sales = Column(Integer, default=0)
    total_purchases = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_online = Column(DateTime(timezone=True))

    # Relationships
    lots = relationship("Lot", back_populates="seller")
    buyer_orders = relationship(
        "Order", foreign_keys="Order.buyer_id", back_populates="buyer"
    )
    seller_orders = relationship(
        "Order", foreign_keys="Order.seller_id", back_populates="seller"
    )
    sent_messages = relationship(
        "Message", foreign_keys="Message.sender_id", back_populates="sender"
    )
    received_messages = relationship(
        "Message", foreign_keys="Message.receiver_id", back_populates="receiver"
    )
    reviews_given = relationship(
        "Review", foreign_keys="Review.reviewer_id", back_populates="reviewer"
    )
    reviews_received = relationship(
        "Review", foreign_keys="Review.reviewed_id", back_populates="reviewed"
    )


class Game(Base):
    """Game model"""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    image_url = Column(String(255))
    icon_url = Column(String(255))

    # Game info
    developer = Column(String(100))
    publisher = Column(String(100))
    release_date = Column(DateTime)
    genres = Column(JSON)  # List of genre strings
    platforms = Column(JSON)  # List of platform strings

    # Stats
    total_lots = Column(Integer, default=0)
    is_popular = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    categories = relationship("Category", back_populates="game")
    lots = relationship("Lot", back_populates="game")


class Category(Base):
    """Category model (types of items in game)"""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), index=True)
    description = Column(Text)
    icon = Column(String(50))  # Icon class or emoji

    # Foreign keys
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"))  # For subcategories

    # Stats
    total_lots = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    game = relationship("Game", back_populates="categories")
    parent = relationship("Category", remote_side=[id])
    children = relationship("Category")
    lots = relationship("Lot", back_populates="category")


class Lot(Base):
    """Lot model (item for sale)"""

    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, index=True)

    # Foreign keys
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Item details
    item_details = Column(JSON)  # Flexible field for game-specific data
    images = Column(JSON)  # List of image URLs

    # Lot settings
    status = Column(SQLEnum(LotStatus), default=LotStatus.MODERATION)
    is_auto_delivery = Column(Boolean, default=False)
    delivery_time = Column(String(50))  # e.g., "1-24 hours"
    requirements = Column(Text)  # Requirements for buyer

    # Stats
    views = Column(Integer, default=0)
    favorites = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    seller = relationship("User", back_populates="lots")
    game = relationship("Game", back_populates="lots")
    category = relationship("Category", back_populates="lots")
    orders = relationship("Order", back_populates="lot")


class Order(Base):
    """Order model"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True)

    # Foreign keys
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lot_id = Column(Integer, ForeignKey("lots.id"), nullable=False)

    # Order details
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    buyer_message = Column(Text)  # Message from buyer
    seller_response = Column(Text)  # Response from seller

    # Escrow info
    escrow_id = Column(String(100))  # External escrow service ID
    payment_method = Column(String(50))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="buyer_orders")
    seller = relationship(
        "User", foreign_keys=[seller_id], back_populates="seller_orders"
    )
    lot = relationship("Lot", back_populates="orders")
    messages = relationship("Message", back_populates="order")
    review = relationship("Review", back_populates="order", uselist=False)


class Message(Base):
    """Message model for chat"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    # Foreign keys
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(
        Integer, ForeignKey("orders.id")
    )  # Optional: message related to order

    # Message info
    is_read = Column(Boolean, default=False)
    is_system = Column(Boolean, default=False)  # System-generated message
    attachments = Column(JSON)  # List of attachment URLs

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_messages"
    )
    order = relationship("Order", back_populates="messages")


class Review(Base):
    """Review model"""

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)

    # Foreign keys
    reviewer_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Who left review
    reviewed_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Who was reviewed
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    # Review info
    is_visible = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    reviewer = relationship(
        "User", foreign_keys=[reviewer_id], back_populates="reviews_given"
    )
    reviewed = relationship(
        "User", foreign_keys=[reviewed_id], back_populates="reviews_received"
    )
    order = relationship("Order", back_populates="review")
