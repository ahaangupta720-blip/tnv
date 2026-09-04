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
echo "Your ~/.tnv/ data will NOT be deleted."
echo

if [ -t 0 ]; then
    read -p "Type UNINSTALL to continue: " confirm

    if [ "$confirm" != "UNINSTALL" ]; then
        echo "Uninstall cancelled."
        exit 0
    fi
else
    echo "Running remote uninstaller..."
    confirm="UNINSTALL"
fi

echo
echo "[1/3] Removing commands..."

sudo rm -f /usr/local/bin/note
sudo rm -f /usr/local/bin/password

echo "[2/3] Removing TNV cache..."

rm -rf "$HOME/.cache/tnv"

echo "[3/3] Finished."

echo
echo "✓ TNV has been uninstalled."
echo
echo "Your notes and password vault were NOT deleted."
echo "They remain in:"
echo
echo "  ~/.tnv/"
