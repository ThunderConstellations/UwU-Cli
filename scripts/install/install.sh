#!/bin/bash
# UwU-CLI Installation Script for Unix/Linux/macOS

echo "Installing UwU-CLI globally..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found: $($PYTHON_CMD --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "ERROR: pip is not available"
        echo "Please ensure pip is installed with Python"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "pip found: $($PIP_CMD --version)"

echo ""
echo "Installing UwU-CLI in development mode..."

# Install in development mode
if $PIP_CMD install -e .; then
    echo ""
    echo "✅ UwU-CLI installed successfully!"
    echo ""
    echo "You can now run UwU-CLI from anywhere using:"
    echo "  uwu-cli"
    echo "  uwu"
    echo ""
    echo "To start using it, simply type:"
    echo "  uwu-cli"
    echo ""
    echo "Installation complete!"
else
    echo "ERROR: Installation failed"
    exit 1
fi 