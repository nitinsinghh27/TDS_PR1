#!/bin/bash

# LLM Code Deployment System - Startup Script

echo "=========================================="
echo "LLM Code Deployment System"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found!"
    echo "   Copy .env.example to .env and configure your credentials"
    echo "   Run: cp .env.example .env"
    echo ""
    read -p "Press Enter to continue anyway (will likely fail) or Ctrl+C to exit..."
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo ""
echo "Starting server..."
echo "Server will be available at: http://localhost:5001"
echo "Health check: http://localhost:5001/"
echo "Deploy endpoint: POST http://localhost:5001/api/deploy"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
