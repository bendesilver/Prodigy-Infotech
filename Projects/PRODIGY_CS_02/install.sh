#!/bin/bash

echo ""
echo "========================================="
echo "   Image Encryption Tool - Installation"
echo "========================================="
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "[✗] Python not found!"
    echo ""
    echo "Please install Python 3.6 or higher:"
    echo "  macOS: brew install python"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3"
    exit 1
fi

echo "[✓] Found Python: $($PYTHON --version)"

# Check pip
if ! $PYTHON -m pip --version &> /dev/null; then
    echo ""
    echo "Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi

echo "[✓] pip is installed"

# Install Pillow
echo ""
echo "Installing Pillow library..."
$PYTHON -m pip install pillow --quiet

if [ $? -eq 0 ]; then
    echo "[✓] Pillow installed successfully"
else
    echo "[✗] Failed to install Pillow"
    echo "Trying alternative method..."
    $PYTHON -m pip install --user pillow
fi

# Make script executable
chmod +x image_tool.py 2>/dev/null || true

echo ""
echo "========================================="
echo "        Installation Complete!"
echo "========================================="
echo ""
echo "To run the tool:"
echo "  ./image_tool.py"
echo "  or"
echo "  python image_tool.py"
echo ""
echo "For command-line usage:"
echo "  ./image_tool.py --help"
echo ""
