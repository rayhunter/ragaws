#!/bin/bash
# Fix Python version issue - recreate venv with Python 3.11/3.12

set -e

echo "🔧 Fixing Python version compatibility issue..."
echo ""

# Check available Python versions
echo "Checking for Python 3.11 or 3.12..."
PYTHON_CMD=""

if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Found Python 3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Found Python 3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    echo "✅ Found Python 3.10"
else
    echo "❌ Python 3.11 or 3.12 not found!"
    echo ""
    echo "Install Python 3.11 with:"
    echo "  brew install python@3.11"
    echo ""
    echo "Or install Python 3.12 with:"
    echo "  brew install python@3.12"
    exit 1
fi

echo ""
echo "Current Python version:"
$PYTHON_CMD --version

echo ""
echo "⚠️  Removing old venv (Python 3.13)..."
cd "$(dirname "$0")"
rm -rf venv

echo ""
echo "📦 Creating new virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the backend:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"

