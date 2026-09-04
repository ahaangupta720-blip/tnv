# TNV

TNV (Terminal Notes & Vault) is a simple terminal-based Notes and Password Vault for Linux and WSL.

No GUI. No complicated menus. Just fast terminal commands.

## Features

### Notes

- Add notes
- List notes
- Show notes
- Search notes
- Edit notes
- Delete notes

### Password Vault

- Encrypted password storage
- Add passwords
- List passwords
- Show passwords
- Edit passwords
- Delete passwords
- Generate secure passwords
- Reset vault

## Installation

Install the requirements:

    sudo apt update
    sudo apt install -y python3 python3-venv

Install TNV:

    curl -fsSL https://raw.githubusercontent.com/ahaangupta720-blip/tnv/main/install.sh | bash

## Notes Commands

    note add "My Note"
    note list
    note show 1
    note search "school"
    note edit 1
    note delete 1

## Password Commands

    password init
    password add github
    password list
    password show github
    password edit github
    password delete github
    password generate
    password reset
