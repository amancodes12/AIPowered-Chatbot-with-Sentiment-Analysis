#!/bin/bash

# ============================================================
# AI Chatbot Environment Setup Script
# Powered by Google Gemini Flash 2.5
# ============================================================

set -e  # Exit on any error

echo "=============================================="
echo "  AI Chatbot - Environment Setup"
echo "  Powered by Google Gemini Flash 2.5"
echo "=============================================="
echo ""

# Configuration
VENV_NAME="venv"
PYTHON_CMD="python3"

# Check if Python is available
if ! command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_CMD="python"
    if ! command -v $PYTHON_CMD &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python 3.8+ from https://www.python.org/"
        exit 1
    fi
fi

echo "✓ Found Python: $($PYTHON_CMD --version)"
echo ""

# Navigate to script directory
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"
echo ""

# Check if virtual environment exists
if [ -d "$VENV_NAME" ]; then
    echo "⚠️  Virtual environment already exists."
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf $VENV_NAME
    else
        echo "Using existing virtual environment."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv $VENV_NAME
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source $VENV_NAME/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Check for API key in config
if grep -q "<YOUR_GEMINI_API_KEY>" config.py 2>/dev/null; then
    echo "=============================================="
    echo "⚠️  IMPORTANT: API Key Configuration Required"
    echo "=============================================="
    echo ""
    echo "You need to set your Google Gemini API key."
    echo ""
    echo "Option 1: Edit config.py directly"
    echo "  Open config.py and replace <YOUR_GEMINI_API_KEY> with your key"
    echo ""
    echo "Option 2: Set environment variable"
    echo "  export GEMINI_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    
    read -p "Enter your Gemini API key (or press Enter to skip): " API_KEY
    if [ ! -z "$API_KEY" ]; then
        # Update config.py with the API key
        sed -i.bak "s/<YOUR_GEMINI_API_KEY>/$API_KEY/" config.py
        rm -f config.py.bak
        echo "✓ API key saved to config.py"
    fi
    echo ""
fi

# Run tests (optional)
read -p "Would you like to run tests? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 Running tests..."
    pytest tests/ -v --tb=short || echo "⚠️  Some tests failed (expected if API key not set)"
    echo ""
fi

# Final instructions
echo "=============================================="
echo "  ✅ Setup Complete!"
echo "=============================================="
echo ""
echo "To start the chatbot:"
echo ""
echo "  1. Activate the virtual environment:"
echo "     source $VENV_NAME/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python app.py"
echo ""
echo "=============================================="
echo ""

# Ask if user wants to run the app
read -p "Would you like to start the chatbot now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting AI Chatbot..."
    echo ""
    python app.py
fi
