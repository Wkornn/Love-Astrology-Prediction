#!/bin/bash

# Kill existing backend
echo "Stopping existing backend..."
pkill -f "uvicorn app.main:app"
sleep 2

# Start new backend
echo "Starting backend..."
cd /Users/biocorn/Documents/GitHub/Love-Astrology-Prediction/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "Backend started on http://localhost:8000"
