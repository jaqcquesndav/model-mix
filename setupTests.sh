#!/bin/bash
# Setup script for test environment

set -e  # Exit on error

echo "================================"
echo "Setting up test environment"
echo "================================"

# Install system dependencies if packages.txt exists
if [ -f "packages.txt" ]; then
    echo "Installing system dependencies from packages.txt..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y $(cat packages.txt | tr '\n' ' ')
        echo "✅ System dependencies installed"
    else
        echo "⚠️  apt-get not found, skipping system dependencies"
    fi
else
    echo "⚠️  packages.txt not found, skipping system dependencies"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --user -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Install test dependencies
echo ""
echo "Installing test dependencies..."
pip install --user pytest pytest-cov pytest-mock
echo "✅ Test dependencies installed"

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import streamlit; print(f'✅ Streamlit version: {streamlit.__version__}')"
python -c "import pandas; print(f'✅ Pandas version: {pandas.__version__}')"
python -c "import lxml; print(f'✅ lxml version: {lxml.__version__}')"
python -c "from bs4 import BeautifulSoup; print('✅ BeautifulSoup4 installed')"
python -c "import pytest; print(f'✅ Pytest version: {pytest.__version__}')"

echo ""
echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "To run tests:"
echo "  pytest"
echo "  pytest -v                    # Verbose output"
echo "  pytest -m unit              # Run only unit tests"
echo "  pytest --cov=. --cov-report=html  # With coverage"
