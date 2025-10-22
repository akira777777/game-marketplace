"""Application constants."""

from typing import Final

# API Configuration
API_V1_PREFIX: Final[str] = "/api/v1"

# Directory Configuration
STATIC_DIRS: Final[dict[str, str]] = {
    "avatars": "avatars",
    "game_images": "game_images",
    "lot_images": "lot_images",
}  # Response Messages
HEALTH_STATUS: Final[str] = "healthy"

# Error Messages
ERROR_MESSAGES: Final[dict[str, str]] = {
    "UNAUTHORIZED": "Authentication required",
    "FORBIDDEN": "Insufficient permissions",
    "NOT_FOUND": "Resource not found",
    "VALIDATION_ERROR": "Invalid input data",
    "INTERNAL_ERROR": "Internal server error",
}

# Success Messages
SUCCESS_MESSAGES: Final[dict[str, str]] = {
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
}
