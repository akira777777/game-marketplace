"""
Database configuration and setup
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from .config import settings

# Sync database engine
engine = create_engine(
    settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=300, echo=settings.DEBUG
)

# Async database engine
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,
)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """Get sync database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        yield session


def init_db():
    """Create all tables in the database."""
    # Import all models to ensure they are registered with Base
    from ..models import User, Game, Category, Lot, Order  # noqa: F401

    Base.metadata.create_all(bind=engine)
