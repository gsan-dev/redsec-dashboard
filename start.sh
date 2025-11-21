#!/bin/bash
# RedSec Dashboard - Start Script for Linux
# This script starts both the backend and frontend development servers

set -e

echo "🚀 Starting RedSec Dashboard..."
echo ""

# Check if we're in the correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the redlab directory"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping RedSec Dashboard..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start backend
echo "📦 Starting Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and start backend on all interfaces
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend on all interfaces
echo "🎨 Starting Frontend..."
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ RedSec Dashboard is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "⚠️  Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait
