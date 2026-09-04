#!/bin/bash

set -e

echo "================================="
echo "        TNV Installer"
echo "================================="
echo

echo "[1/5] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed."
    echo "Install it with:"
    echo "  sudo apt install python3 python3-venv"
    exit 1
fi

echo "[2/5] Creating Python environment..."

python3 -m venv "$HOME/.tnv/venv"

echo "[3/5] Installing Python dependencies..."

"$HOME/.tnv/venv/bin/pip" install --upgrade pip
"$HOME/.tnv/venv/bin/pip" install cryptography

echo "[4/5] Creating directories..."

mkdir -p "$HOME/.tnv/notes"

echo "[5/5] Installing commands..."

sudo cp password.py /usr/local/bin/password
sudo cp tnv.py /usr/local/bin/note

sudo sed -i "1c\\#!$HOME/.tnv/venv/bin/python" /usr/local/bin/password
sudo sed -i "1c\\#!$HOME/.tnv/venv/bin/python" /usr/local/bin/note

sudo chmod +x /usr/local/bin/password
sudo chmod +x /usr/local/bin/note

echo
echo "================================="
echo "      TNV Installation Done!"
echo "================================="
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
