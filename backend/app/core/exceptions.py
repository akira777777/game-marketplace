"""Custom exceptions for the application."""

from typing import Any, Dict, Optional


class GameMarketplaceException(Exception):
    """Base exception for GameMarketplace application."""

    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code


class ValidationException(GameMarketplaceException):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field, **(details or {})},
            status_code=400,
        )


class AuthenticationException(GameMarketplaceException):
    """Exception raised for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication required",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            details=details,
            status_code=401,
        )


class AuthorizationException(GameMarketplaceException):
    """Exception raised for authorization errors."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        required_role: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            details={"required_role": required_role, **(details or {})},
            status_code=403,
        )


class ResourceNotFoundException(GameMarketplaceException):
    """Exception raised when a resource is not found."""

    def __init__(
        self, resource_type: str, resource_id: Any, message: Optional[str] = None
    ):
        message = message or f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            error_code="RESOURCE_NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id},
            status_code=404,
        )


class BusinessLogicException(GameMarketplaceException):
    """Exception raised for business logic violations."""

    def __init__(
        self,
        message: str,
        rule: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="BUSINESS_LOGIC_ERROR",
            details={"rule": rule, **(details or {})},
            status_code=422,
        )


class ExternalServiceException(GameMarketplaceException):
    """Exception raised for external service failures."""

    def __init__(
        self,
        service_name: str,
        message: str = "External service unavailable",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=f"{service_name}: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service_name, **(details or {})},
            status_code=503,
        )


class RateLimitException(GameMarketplaceException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, limit: int, window: str, message: Optional[str] = None):
        message = message or f"Rate limit exceeded: {limit} requests per {window}"
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            details={"limit": limit, "window": window},
            status_code=429,
        )


class DatabaseException(GameMarketplaceException):
    """Exception raised for database operation errors."""

    def __init__(
        self,
        operation: str,
        message: str = "Database operation failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=f"Database {operation}: {message}",
            error_code="DATABASE_ERROR",
            details={"operation": operation, **(details or {})},
            status_code=500,
        )


class FileUploadException(GameMarketplaceException):
    """Exception raised for file upload errors."""

    def __init__(
        self, filename: str, reason: str, details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"File upload failed for '{filename}': {reason}",
            error_code="FILE_UPLOAD_ERROR",
            details={"filename": filename, "reason": reason, **(details or {})},
            status_code=400,
        )
