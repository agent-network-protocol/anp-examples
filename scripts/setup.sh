#!/bin/bash

# UV Environment Setup Script for ANP Examples Project

echo "🚀 Setting up ANP Examples project with UV..."

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ UV version: $(uv --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
else
    echo "✅ Virtual environment already exists"
fi

# Install dependencies
echo "🔧 Installing dependencies..."
source .venv/bin/activate
uv pip install -e .

# Install dev dependencies
echo "🔧 Installing dev dependencies..."
uv pip install pytest

echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To run the project:"
echo "  uv run python your_script.py" 