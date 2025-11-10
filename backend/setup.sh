#!/bin/bash
# Backend setup script - installs dependencies and activates virtual environment

set -e

cd "$(dirname "$0")"

echo "🔧 Setting up backend environment..."

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To run the backend:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Or use the Makefile:"
echo "  make dev-backend"

