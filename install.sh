#!/bin/bash
# install.sh - Setup script for SUMOT word game application

echo "=========================================="
echo "       SUMOT Installation Script"
echo "=========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Determine Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "Detected Python version: $PYTHON_VERSION"

# Try to install python3-venv (generic version)
echo "Installing python3-venv package..."
sudo apt update
if ! sudo apt install -y python3-venv; then
    echo "Failed to install python3-venv. Trying specific version package..."
    # Try version-specific venv
    if ! sudo apt install -y python$PYTHON_VERSION-venv; then
        echo "Failed to install Python virtual environment packages."
        echo "Please try to install it manually with:"
        echo "  sudo apt install python3-venv"
        exit 1
    fi
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Please check Python installation."
    exit 1
fi

# Determine the activate command based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if data directories exist
if [ ! -d "app/dico" ]; then
    echo "Creating dictionary directories..."
    mkdir -p app/dico
fi

# Display success message
echo
echo "=========================================="
echo "Installation complete!"
echo
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python app/app.py"
echo
echo "Or using Docker:"
echo "  docker compose up -d --build"
echo "=========================================="