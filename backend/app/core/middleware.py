"""Custom middleware for the application."""

import time
import uuid
from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .logging import log_api_request, get_logger
from .constants import ERROR_MESSAGES
from .exceptions import GameMarketplaceException

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging API requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log metrics."""
        start_time = time.time()

        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        if "x-forwarded-for" in request.headers:
            client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

        # Log request start
        logger.info(f"Request {request_id} started: {request.method} {request.url}")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log access information
            log_api_request(
                client_ip=client_ip,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time=process_time,
                request_id=request_id,
            )

            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time, 3))

            return response

        except Exception as exc:
            process_time = time.time() - start_time

            logger.error(
                f"Request {request_id} failed: {exc}",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "process_time": process_time,
                },
            )

            # Log failed request
            log_api_request(
                client_ip=client_ip,
                method=request.method,
                url=str(request.url),
                status_code=500,
                process_time=process_time,
                request_id=request_id,
                error=str(exc),
            )

            # Return structured error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": ERROR_MESSAGES["INTERNAL_ERROR"],
                    "request_id": request_id,
                    "detail": str(exc) if logger.level <= 10 else None,  # Debug level
                },
                headers={"X-Request-ID": request_id},
            )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle errors globally."""
        try:
            return await call_next(request)
        except HTTPException:
            # Re-raise HTTP exceptions to be handled by FastAPI
            raise
        except ValueError as exc:
            logger.warning(f"Validation error: {exc}")
            return JSONResponse(
                status_code=400,
                content={
                    "error": ERROR_MESSAGES["VALIDATION_ERROR"],
                    "detail": str(exc),
                },
            )
        except PermissionError as exc:
            logger.warning(f"Permission error: {exc}")
            return JSONResponse(
                status_code=403,
                content={"error": ERROR_MESSAGES["FORBIDDEN"], "detail": str(exc)},
            )
        except Exception as exc:
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(
                f"Unhandled error in request {request_id}: {exc}", exc_info=True
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": ERROR_MESSAGES["INTERNAL_ERROR"],
                    "request_id": request_id,
                },
            )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to responses."""
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'"
        )

        return response
