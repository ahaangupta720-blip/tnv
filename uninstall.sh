#!/bin/bash

set -e

echo "================================="
echo "        TNV Uninstaller"
echo "================================="
echo

echo "This will remove:"
echo "  - note command"
echo "  - password command"
echo "  - TNV installation files"
echo

read -p "Type UNINSTALL to continue: " confirm

if [ "$confirm" != "UNINSTALL" ]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo
echo "[1/3] Removing commands..."

sudo rm -f /usr/local/bin/note
sudo rm -f /usr/local/bin/password

echo "[2/3] Removing Python cache..."

rm -rf "$HOME/.cache/tnv"

echo "[3/3] Installation commands removed."

echo
echo "✓ TNV has been uninstalled."
echo
echo "Your vault and notes were NOT deleted."
echo "They remain in:"
echo
echo "  ~/.tnv/"
echo
echo "================================="
