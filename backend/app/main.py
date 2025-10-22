"""Main FastAPI application."""

import os
from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import auth, users, games, lots, orders
from .core.config import settings
from .core.constants import API_V1_PREFIX, STATIC_DIRS, HEALTH_STATUS
from .core.database import engine, Base
from .core.logging import setup_logging, get_logger
from .core.middleware import (
    RequestLoggingMiddleware,
    ErrorHandlingMiddleware,
    SecurityHeadersMiddleware,
)

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Build FastAPI app
app = FastAPI(
    title=getattr(settings, "APP_NAME", "GameMarketplace API"),
    description=getattr(
        settings, "DESCRIPTION", "A marketplace for gaming items and services"
    ),
    version=getattr(settings, "VERSION", "1.0.0"),
    docs_url=getattr(settings, "DOCS_URL", "/docs"),
    redoc_url=getattr(settings, "REDOC_URL", "/redoc"),
)

# Add custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS middleware
allowed_origins: List[str] = getattr(settings, "CORS_ORIGINS", ["*"])
# Настройка CORS для production и development
cors_origins = ["http://localhost:3000", "http://localhost:4000"]
if os.getenv("ENVIRONMENT") == "production":
    cors_origins.append("https://cheerful-cocada-c90721.netlify.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static directory setup
static_dir = getattr(settings, "UPLOAD_DIR", "static")
os.makedirs(static_dir, exist_ok=True)

# Create static subdirectories
for subdir in STATIC_DIRS.values():
    os.makedirs(os.path.join(static_dir, subdir), exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": getattr(settings, "APP_NAME", "GameMarketplace API"),
        "version": getattr(settings, "VERSION", "1.0.0"),
        "status": "running",
        "docs": getattr(settings, "DOCS_URL", "/docs"),
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": HEALTH_STATUS}


# Include API routers
app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(users.router, prefix=API_V1_PREFIX)
app.include_router(games.router, prefix=API_V1_PREFIX)
app.include_router(lots.router, prefix=API_V1_PREFIX)
app.include_router(orders.router, prefix=API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend/app/main.py",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
