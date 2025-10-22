"""
Pydantic schemas for API data validation
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any, Generic, TypeVar
from datetime import datetime
from decimal import Decimal
from enum import Enum


# Enums for schemas
class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class LotStatus(str, Enum):
    ACTIVE = "active"
    SOLD = "sold"
    INACTIVE = "inactive"
    MODERATION = "moderation"


class UserRole(str, Enum):
    USER = "user"
    SELLER = "seller"
    MODERATOR = "moderator"
    ADMIN = "admin"


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseSchema):
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: str = Field(..., min_length=8, description="User password")


class UserUpdate(BaseSchema):
    """Schema for updating user"""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """Schema for user response"""

    id: int
    role: str
    is_active: bool
    is_verified: bool
    rating: float
    reviews_count: int
    created_at: datetime
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseSchema):
    """Schema for user login"""

    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


# Token schemas
class Token(BaseSchema):
    """Token response schema"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseSchema):
    """Token refresh schema"""

    refresh_token: str


class TokenData(BaseSchema):
    """Token data schema"""

    user_id: int
    username: str


class Message(BaseSchema):
    """Generic message response schema"""

    message: str


class UserPublic(UserBase):
    id: int
    avatar_url: Optional[str] = None
    is_verified: bool
    role: UserRole
    rating: float
    total_reviews: int
    total_sales: int
    created_at: datetime
    last_online: Optional[datetime] = None


class UserPrivate(UserPublic):
    total_purchases: int
    is_active: bool


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginRequest(BaseSchema):
    username: str
    password: str


# Game schemas
class GameBase(BaseSchema):
    name: str
    description: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    genres: Optional[List[str]] = []
    platforms: Optional[List[str]] = []


class GameCreate(GameBase):
    slug: str


class GameUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    genres: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Game(GameBase):
    id: int
    slug: str
    image_url: Optional[str] = None
    icon_url: Optional[str] = None
    total_lots: int
    is_popular: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GameResponse(Game):
    """Schema for game response"""

    pass


# Category schemas
class CategoryBase(BaseSchema):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    game_id: int
    parent_id: Optional[int] = None
    slug: str


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class Category(CategoryBase):
    id: int
    slug: str
    game_id: int
    parent_id: Optional[int] = None
    total_lots: int
    is_active: bool
    sort_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryResponse(Category):
    """Schema for category response"""

    pass


# Lot schemas
class LotBase(BaseSchema):
    title: str
    description: str
    price: Decimal
    delivery_time: Optional[str] = None
    requirements: Optional[str] = None
    is_auto_delivery: bool = False


class LotCreate(LotBase):
    game_id: int
    category_id: int
    item_details: Optional[Dict[str, Any]] = {}
    images: Optional[List[str]] = []


class LotUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    delivery_time: Optional[str] = None
    requirements: Optional[str] = None
    is_auto_delivery: Optional[bool] = None
    item_details: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    status: Optional[LotStatus] = None


class Lot(LotBase):
    id: int
    seller_id: int
    game_id: int
    category_id: int
    item_details: Dict[str, Any]
    images: List[str]
    status: LotStatus
    views: int
    favorites: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Related data
    seller: Optional[UserPublic] = None
    game: Optional[Game] = None
    category: Optional[Category] = None


class LotList(BaseSchema):
    """Schema for lot listings with minimal data"""

    id: int
    title: str
    price: Decimal
    seller_id: int
    game_id: int
    category_id: int
    status: LotStatus
    views: int
    favorites: int
    created_at: datetime
    seller_username: Optional[str] = None
    seller_rating: Optional[float] = None
    game_name: Optional[str] = None
    category_name: Optional[str] = None


# Order schemas
class OrderBase(BaseSchema):
    buyer_message: Optional[str] = None


class OrderCreate(OrderBase):
    lot_id: int


class OrderUpdate(BaseSchema):
    status: Optional[OrderStatus] = None
    seller_response: Optional[str] = None


class Order(OrderBase):
    id: int
    order_number: str
    buyer_id: int
    seller_id: int
    lot_id: int
    price: Decimal
    status: OrderStatus
    seller_response: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Related data
    buyer: Optional[UserPublic] = None
    seller: Optional[UserPublic] = None
    lot: Optional[Lot] = None


# Message schemas
class MessageBase(BaseSchema):
    content: str


class MessageCreate(MessageBase):
    receiver_id: int
    order_id: Optional[int] = None


class Message(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    order_id: Optional[int] = None
    is_read: bool
    is_system: bool
    attachments: Optional[List[str]] = []
    created_at: datetime

    # Related data
    sender: Optional[UserPublic] = None


# Review schemas
class ReviewBase(BaseSchema):
    rating: int
    comment: Optional[str] = None

    @validator("rating")
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewCreate(ReviewBase):
    order_id: int


class Review(ReviewBase):
    id: int
    reviewer_id: int
    reviewed_id: int
    order_id: int
    is_visible: bool
    created_at: datetime

    # Related data
    reviewer: Optional[UserPublic] = None


# Search and filter schemas
class LotFilters(BaseSchema):
    game_id: Optional[int] = None
    category_id: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    search: Optional[str] = None
    seller_id: Optional[int] = None
    status: Optional[LotStatus] = None


class LotSort(str, Enum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    DATE_DESC = "date_desc"
    DATE_ASC = "date_asc"
    POPULAR = "popular"
    RATING = "rating"


# Pagination schemas
class PaginationParams(BaseSchema):
    page: int = 1
    size: int = 20

    @validator("page")
    def validate_page(cls, v):
        if v < 1:
            raise ValueError("Page must be greater than 0")
        return v

    @validator("size")
    def validate_size(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Size must be between 1 and 100")
        return v


# Generic type for pagination
T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response schema"""

    items: List[T]
    total: int
    skip: int
    limit: int

# Response schemas (inherit from main classes with from_attributes=True)
class LotResponse(Lot):
    """Schema for lot response"""
    class Config:
        from_attributes = True

class OrderResponse(Order):
    """Schema for order response"""  
    class Config:
        from_attributes = True

class ReviewResponse(Review):
    """Schema for review response"""
    class Config:
        from_attributes = True

class MessageResponse(Message):
    """Schema for message response"""
    class Config:
        from_attributes = True
