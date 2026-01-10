#!/bin/bash

# Script to kill the Flask application
# Reads PORT from .env file

cd "$(dirname "$0")"

# Load environment variables from .env (skip comments and empty lines)
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
    PORT=${PORT:-8000}
else
    PORT=8000
    echo "⚠️  Warning: .env file not found, using default port 8000"
fi

echo "Attempting to stop the application on port $PORT..."
echo ""

# Method 1: Find and kill processes using the specific port
echo "Method 1: Killing processes on port $PORT..."
pids=$(lsof -ti:$PORT)

if [ -z "$pids" ]; then
    echo "❌ No process found on port $PORT"
else
    echo "Found process(es): $pids"
    for pid in $pids; do
        echo "Killing process $pid..."
        kill -15 $pid 2>/dev/null
        sleep 1
        if kill -0 $pid 2>/dev/null; then
            echo "Force killing process $pid..."
            kill -9 $pid
        fi
    done
    echo "✅ Process(es) on port $PORT have been stopped"
fi

# Method 2: Also kill any python process running app.py
echo ""
echo "Method 2: Killing any app.py processes..."
pkill -f "python.*app.py" || true
echo "✅ All app.py processes have been stopped"

echo ""
echo "Application stopped successfully!"
exit 0
