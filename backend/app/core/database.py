"""Database configuration and session management."""

import logging
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from .config import settings

logger = logging.getLogger(__name__)

# PostgreSQL (Neon) configuration
# Engine configuration
engine_kwargs = {
    "pool_pre_ping": True,
    "echo": settings.DATABASE_ECHO,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

# Database engines
engine = create_engine(
    settings.database_url_sync,
    **engine_kwargs
)

# Async engine with appropriate configuration
async_engine_kwargs = {
    "echo": settings.DATABASE_ECHO,
    "pool_size": 5,
    "max_overflow": 10,
}

async_engine = create_async_engine(
    settings.database_url_async,
    **async_engine_kwargs
)

# Session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models - updated for SQLAlchemy 2.0
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get sync database session"""
    db = SessionLocal()
    try:
        logger.debug("Creating database session")
        yield db
        logger.debug("Database session completed successfully")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            logger.debug("Creating async database session")
            yield session
            logger.debug("Async database session completed successfully")
        except Exception as e:
            logger.error(f"Async database session error: {e}")
            await session.rollback()
            raise


def init_db():
    """Create all tables in the database."""
    try:
        logger.info("Starting database initialization...")

        # Import all models to ensure they are registered with Base
        from ..models import (
            User, Game, Category, Lot, Order, Message, Review  # noqa: F401
        )

        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
