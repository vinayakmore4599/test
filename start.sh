#!/bin/bash

# Script to start the Flask application
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

echo "Starting Flask application on port $PORT..."
echo ""

python3 app.py $PORT
