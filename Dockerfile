# Production-grade multi-stage Dockerfile for GameMarketplace
FROM python:3.11-slim as builder

# Build arguments
ARG POETRY_VERSION=1.7.1

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Set work directory
WORKDIR /app

# Copy dependency files
COPY backend/requirements.txt pyproject.toml poetry.lock* ./

# Install dependencies
RUN if [ -f "poetry.lock" ]; then \
        poetry install --no-dev --no-root; \
    else \
        pip install -r requirements.txt; \
    fi

# Remove cache
RUN rm -rf $POETRY_CACHE_DIR

# Production stage
FROM python:3.11-slim as production

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY backend/ ./backend/
COPY static/ ./static/

# Create necessary directories
RUN mkdir -p logs static/uploads/{avatars,game_images,lot_images} \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]