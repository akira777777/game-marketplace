"""Logging configuration for the application."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

from .config import settings


def setup_logging() -> logging.Logger:
    """Configure application logging with rotation and structured format."""

    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Define log format
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(pathname)s:%(lineno)d - %(message)s"
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(settings, "LOG_LEVEL", "INFO"))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)

    # API access log handler
    access_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "access.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding="utf-8",
    )
    access_handler.setLevel(logging.INFO)
    access_formatter = logging.Formatter(
        "%(asctime)s - %(client_ip)s - %(method)s %(url)s - "
        "%(status_code)s - %(process_time)ss"
    )
    access_handler.setFormatter(access_formatter)

    # Create separate logger for access logs
    access_logger = logging.getLogger("access")
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(access_handler)
    access_logger.propagate = False

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


def log_api_request(
    client_ip: str,
    method: str,
    url: str,
    status_code: int,
    process_time: float,
    **kwargs: Any
) -> None:
    """Log API request information."""
    access_logger = logging.getLogger("access")

    # Use LoggerAdapter to add extra fields
    adapter = logging.LoggerAdapter(
        access_logger,
        {
            "client_ip": client_ip,
            "method": method,
            "url": url,
            "status_code": status_code,
            "process_time": round(process_time, 3),
            **kwargs,
        },
    )

    adapter.info("")
