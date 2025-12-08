#!/bin/bash

# T0OL-B4S3-263 WhatsApp C2 Quick Install Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     T0OL-B4S3-263 WhatsApp C2 - Quick Installer           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Windows (Git Bash)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "[*] Detected Windows environment"
    PYTHON="python"
    NPM="npm.cmd"
else
    echo "[*] Detected Unix-like environment"
    PYTHON="python3"
    NPM="npm"
fi

# Install Python dependencies
echo "[*] Installing Python dependencies..."
$PYTHON -m pip install flask flask-cors cryptography

# Create whatsapp-c2 directory if it doesn't exist
if [ ! -d "whatsapp-c2" ]; then
    echo "[*] Creating whatsapp-c2 directory..."
    mkdir -p whatsapp-c2
fi

# Setup Node.js project
echo "[*] Setting up Node.js project..."
cd whatsapp-c2

# Create package.json if it doesn't exist
if [ ! -f "package.json" ]; then
    echo "[*] Initializing npm project..."
    $NPM init -y
fi

# Install Node.js dependencies
echo "[*] Installing Node.js dependencies..."
$NPM install @whiskeysockets/baileys@latest axios qrcode-terminal pino chalk moment sharp form-data

# Create directories
mkdir -p utils
mkdir -p sessions

cd ..

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  INSTALLATION COMPLETE!                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Copy all bot files to whatsapp-c2/ directory"
echo "2. Edit config.json with your settings"
echo "3. Run: python start_whatsapp_c2.py"
echo ""