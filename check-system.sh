#!/bin/bash

echo "🚀 Love Debugging Lab v2.0 - Quick Start"
echo "========================================"
echo ""

# Check if backend is running
echo "Checking backend..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on port 8000"
else
    echo "❌ Backend is NOT running"
    echo "   Start it with: cd backend && uvicorn app.main:app --reload"
    exit 1
fi

# Check if frontend is running
echo "Checking frontend..."
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend is running on port 5173"
else
    echo "❌ Frontend is NOT running"
    echo "   Start it with: cd frontend && npm run dev"
    exit 1
fi

echo ""
echo "✅ All systems operational!"
echo ""
echo "📍 Access Points:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🧪 Test Data:"
echo "   Date: 1990-06-15"
echo "   Time: 14:30"
echo "   Lat:  40.7128"
echo "   Lon:  -74.0060"
echo ""
echo "🎉 Ready to test!"
