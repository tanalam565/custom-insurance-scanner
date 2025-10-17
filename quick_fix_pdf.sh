#!/bin/bash

echo "============================================================"
echo "PDF Support Quick Fix"
echo "============================================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected: Linux"
    echo ""
    
    echo "Step 1: Installing Poppler..."
    sudo apt-get update
    sudo apt-get install -y poppler-utils
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    echo ""
    
    echo "Step 1: Installing Poppler..."
    if ! command -v brew &> /dev/null; then
        echo "ERROR: Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi
    brew install poppler
    
else
    echo "ERROR: Unsupported operating system: $OSTYPE"
    exit 1
fi

echo ""
echo "Step 2: Installing Python dependencies..."
pip install pdf2image PyPDF2

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python packages"
    exit 1
fi

echo ""
echo "Step 3: Verifying installation..."
if command -v pdftoppm &> /dev/null; then
    echo "✓ Poppler installed successfully"
else
    echo "✗ Poppler installation failed"
    exit 1
fi

python -c "import pdf2image; print('✓ pdf2image installed')" 2>/dev/null || echo "✗ pdf2image not found"
python -c "import PyPDF2; print('✓ PyPDF2 installed')" 2>/dev/null || echo "✗ PyPDF2 not found"

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "You can now:"
echo "1. Restart your application: python app.py"
echo "2. Upload PDF files"
echo ""