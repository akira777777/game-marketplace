#!/bin/bash
cd /mnt/games/Projects/python-dev-env/GameMarketplace
source venv/bin/activate
export PYTHONPATH=/mnt/games/Projects/python-dev-env/GameMarketplace
uvicorn backend.app.main:app --host 0.0.0.0 --port 8001 --reload