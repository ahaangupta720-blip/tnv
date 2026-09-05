#!/bin/bash

set -e

echo "================================="
echo "        TNV Installer"
echo "================================="
echo

echo "[1/5] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed."
    exit 1
fi

echo "[2/5] Detecting environment..."

if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
    echo "Termux detected."
    INSTALL_DIR="$PREFIX/bin"
elif [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo "Termux detected."
    INSTALL_DIR="/data/data/com.termux/files/usr/bin"
else
    echo "Linux/WSL detected."
    INSTALL_DIR="/usr/local/bin"
fi

echo "[3/5] Creating Python environment..."

mkdir -p "$HOME/.tnv"

if [ ! -d "$HOME/.tnv/venv" ]; then
    python3 -m venv "$HOME/.tnv/venv"
fi

echo "[4/5] Installing Python dependencies..."

"$HOME/.tnv/venv/bin/pip" install --upgrade pip
"$HOME/.tnv/venv/bin/pip" install cryptography

echo "[5/5] Installing commands..."

mkdir -p "$HOME/.tnv/notes"

TEMP_DIR="$(mktemp -d)"

curl -fsSL https://raw.githubusercontent.com/ahaangupta720-blip/tnv/main/password.py \
    -o "$TEMP_DIR/password"

curl -fsSL https://raw.githubusercontent.com/ahaangupta720-blip/tnv/main/tnv.py \
    -o "$TEMP_DIR/note"

sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$TEMP_DIR/password"
sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$TEMP_DIR/note"

chmod +x "$TEMP_DIR/password"
chmod +x "$TEMP_DIR/note"

if [ "$INSTALL_DIR" = "/usr/local/bin" ]; then
    sudo cp "$TEMP_DIR/password" "$INSTALL_DIR/password"
    sudo cp "$TEMP_DIR/note" "$INSTALL_DIR/note"
else
    cp "$TEMP_DIR/password" "$INSTALL_DIR/password"
    cp "$TEMP_DIR/note" "$INSTALL_DIR/note"
fi

rm -rf "$TEMP_DIR"

echo
echo "================================="
echo "      TNV Installation Done!"
echo "================================="
echo
echo "Commands installed:"
echo
echo "  note"
echo "  password"
echo
echo "Try:"
echo
echo "  note help"
echo "  password help"
echo
