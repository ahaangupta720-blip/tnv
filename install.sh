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

echo "[2/5] Creating Python environment..."

mkdir -p "$HOME/.tnv"

if [ ! -d "$HOME/.tnv/venv" ]; then
    python3 -m venv "$HOME/.tnv/venv"
fi

echo "[3/5] Installing Python dependencies..."

"$HOME/.tnv/venv/bin/pip" install --upgrade pip
"$HOME/.tnv/venv/bin/pip" install cryptography

echo "[4/5] Creating directories..."

mkdir -p "$HOME/.tnv/notes"

echo "[5/5] Installing commands..."

if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
    echo "Termux detected."

    INSTALL_DIR="$PREFIX/bin"

    cp "$OLDPWD/password.py" "$INSTALL_DIR/password"
    cp "$OLDPWD/tnv.py" "$INSTALL_DIR/note"

    chmod +x "$INSTALL_DIR/password"
    chmod +x "$INSTALL_DIR/note"

    sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$INSTALL_DIR/password"
    sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$INSTALL_DIR/note"

else
    echo "Linux/WSL detected."

    INSTALL_DIR="/usr/local/bin"

    sudo cp "$OLDPWD/password.py" "$INSTALL_DIR/password"
    sudo cp "$OLDPWD/tnv.py" "$INSTALL_DIR/note"

    sudo chmod +x "$INSTALL_DIR/password"
    sudo chmod +x "$INSTALL_DIR/note"

    sudo sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$INSTALL_DIR/password"
    sudo sed -i "1c\\#!$HOME/.tnv/venv/bin/python" "$INSTALL_DIR/note"
fi

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
