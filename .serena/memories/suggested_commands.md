# Suggested Commands and Operations

## Development Commands

### Server Management
```bash
# Start backend server
cd /mnt/games/Projects/python-dev-env/GameMarketplace
source venv/bin/activate
export PYTHONPATH=/mnt/games/Projects/python-dev-env/GameMarketplace
uvicorn backend.app.main:app --host 0.0.0.0 --port 8001 --reload

# Or use the provided script
./start_server.sh
```

### Testing
```bash
# Backend tests (when implemented)
cd backend
pytest

# Test server response
curl http://localhost:8001
curl http://localhost:8001/health
curl http://localhost:8001/docs
```

### Database Operations
```bash
# Database migrations (when Alembic is configured)
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

### Code Quality
```bash
# Code formatting (tools available in requirements)
cd backend
black app/
isort app/
flake8 app/
```

### Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

## Debugging Commands
```bash
# Check running processes
ps aux | grep uvicorn

# Check port usage
lsof -i :8001

# View logs
tail -f server.log

# Test API endpoints
curl -s http://localhost:8001/api/v1/games | python -m json.tool
```

## Git Operations
```bash
git status
git add .
git commit -m "Description"
git push origin feature/branch-name
```