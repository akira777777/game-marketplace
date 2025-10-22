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

# Database engines
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DATABASE_ECHO,
)

async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=settings.DATABASE_ECHO,
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
