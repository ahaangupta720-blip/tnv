#!/bin/bash

set -e

echo "================================="
echo "        TNV Installer"
echo "================================="
echo

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed."
    echo "Please install Python3 first."
    exit 1
fi

echo "[1/5] Installing Python dependencies..."

python3 -m pip install --user cryptography

echo "[2/5] Creating directories..."

mkdir -p "$HOME/.tnv/notes"

echo "[3/5] Installing commands..."

sudo cp password.py /usr/local/bin/password
sudo cp tnv.py /usr/local/bin/note

sudo chmod +x /usr/local/bin/password
sudo chmod +x /usr/local/bin/note

echo "[4/5] Checking installation..."

if command -v password >/dev/null 2>&1; then
    echo "✓ password installed"
else
    echo "✗ password installation failed"
    exit 1
fi

if command -v note >/dev/null 2>&1; then
    echo "✓ note installed"
else
    echo "✗ note installation failed"
    exit 1
fi

echo "[5/5] Installation complete!"
echo
echo "You can now use:"
echo
echo "  note list"
echo "  note add \"My Note\""
echo
echo "  password init"
echo "  password add github"
echo "  password list"
echo "  password generate"
echo
echo "================================="
echo "        Installation Done!"
echo "================================="
