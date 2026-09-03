#!/usr/bin/env python3

import os
import sys
import json
import base64
import secrets
import string
import getpass
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = os.path.expanduser("~/.tnv")
VAULT_FILE = os.path.join(BASE_DIR, "vault.enc")

os.makedirs(BASE_DIR, exist_ok=True)


# ============================================================
# HELP
# ============================================================

def help_command():
    print("""
Password Vault
==============

password init
    Create a new encrypted password vault.

password add <name>
    Add a password entry.

password list
    List all saved entries.

password show <name>
    Show a saved password entry.

password edit <name>
    Edit an existing entry.

password delete <name>
    Delete an entry.

password generate
    Generate a secure random password.

password reset
    Permanently delete the entire vault.

password help
    Show this help message.
""")


# ============================================================
# KEY DERIVATION
# ============================================================

def derive_key(master_password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        600_000,
        32
    )


# ============================================================
# VAULT CHECK
# ============================================================

def vault_exists():
    return os.path.isfile(VAULT_FILE)


# ============================================================
# CREATE VAULT
# ============================================================

def create_vault():

    if vault_exists():
        print("✗ A vault already exists.")
        print("Use 'password reset' if you want to delete it.")
        return

    print("=== Create Password Vault ===")
    print()

    while True:
        master = getpass.getpass("Create master password: ")

        if len(master) < 8:
            print("✗ Master password must be at least 8 characters.")
            continue

        confirm = getpass.getpass("Confirm master password: ")

        if master != confirm:
            print("✗ Passwords do not match.")
            continue

        break

    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)

    key = derive_key(master, salt)

    aes = AESGCM(key)

    empty_data = {
        "entries": {}
    }

    plaintext = json.dumps(empty_data).encode("utf-8")

    encrypted = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    vault = {
        "version": 1,
        "salt": base64.b64encode(salt).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "data": base64.b64encode(encrypted).decode("utf-8")
    }

    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f)

    os.chmod(VAULT_FILE, 0o600)

    print()
    print("✓ Vault created successfully.")
    print("Vault location:", VAULT_FILE)


# ============================================================
# UNLOCK VAULT
# ============================================================

def unlock_vault():

    if not vault_exists():
        print("✗ No vault exists.")
        print("Run 'password init' first.")
        return None

    master = getpass.getpass("Master password: ")

    try:
        with open(VAULT_FILE, "r") as f:
            vault = json.load(f)

        salt = base64.b64decode(vault["salt"])
        nonce = base64.b64decode(vault["nonce"])
        encrypted = base64.b64decode(vault["data"])

        key = derive_key(master, salt)

        aes = AESGCM(key)

        plaintext = aes.decrypt(
            nonce,
            encrypted,
            None
        )

        data = json.loads(
            plaintext.decode("utf-8")
        )

        return data

    except Exception:
        print("✗ Incorrect master password.")
        return None


# ============================================================
# SAVE VAULT
# ============================================================

def save_vault(data):

    try:
        with open(VAULT_FILE, "r") as f:
            old_vault = json.load(f)

        salt = base64.b64decode(
            old_vault["salt"]
        )

        master = getpass.getpass(
            "Enter master password to save: "
        )

        key = derive_key(master, salt)

        aes = AESGCM(key)

        nonce = secrets.token_bytes(12)

        plaintext = json.dumps(
            data
        ).encode("utf-8")

        encrypted = aes.encrypt(
            nonce,
            plaintext,
            None
        )

        vault = {
            "version": 1,
            "salt": base64.b64encode(
                salt
            ).decode("utf-8"),

            "nonce": base64.b64encode(
                nonce
            ).decode("utf-8"),

            "data": base64.b64encode(
                encrypted
            ).decode("utf-8")
        }

        with open(VAULT_FILE, "w") as f:
            json.dump(vault, f)

        os.chmod(VAULT_FILE, 0o600)

        return True

    except Exception as e:
        print("✗ Failed to save vault.")
        print(e)
        return False


# ============================================================
# ADD PASSWORD
# ============================================================

def add_password(name):

    if not name:
        print("Usage: password add <name>")
        return

    data = unlock_vault()

    if data is None:
        return

    entries = data.setdefault("entries", {})

    if name in entries:
        print(f"✗ Entry '{name}' already exists.")
        print("Use 'password edit " + name + "' instead.")
        return

    print()
    print(f"=== Add Password: {name} ===")
    print()

    username = input("Username: ")

    password = getpass.getpass(
        "Password: "
    )

    url = input("URL: ")

    notes = input("Notes: ")

    entries[name] = {
        "username": username,
        "password": password,
        "url": url,
        "notes": notes
    }

    if save_vault(data):
        print()
        print(f"✓ Password '{name}' saved.")


# ============================================================
# LIST PASSWORDS
# ============================================================

def list_passwords():

    data = unlock_vault()

    if data is None:
        return

    entries = data.get("entries", {})

    if not entries:
        print("Vault is empty.")
        return

    print()
    print("Saved passwords:")
    print()

    names = sorted(entries.keys())

    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")

    print()
    print(f"Total: {len(names)}")


# ============================================================
# SHOW PASSWORD
# ============================================================

def show_password(name):

    if not name:
        print("Usage: password show <name>")
        return

    data = unlock_vault()

    if data is None:
        return

    entries = data.get("entries", {})

    if name not in entries:
        print(f"✗ Entry '{name}' not found.")
        return

    entry = entries[name]

    print()
    print("==============================")
    print(f"Name:     {name}")
    print(f"Username: {entry.get('username', '')}")
    print(f"Password: {entry.get('password', '')}")
    print(f"URL:      {entry.get('url', '')}")
    print(f"Notes:    {entry.get('notes', '')}")
    print("==============================")


# ============================================================
# EDIT PASSWORD
# ============================================================

def edit_password(name):

    if not name:
        print("Usage: password edit <name>")
        return

    data = unlock_vault()

    if data is None:
        return

    entries = data.get("entries", {})

    if name not in entries:
        print(f"✗ Entry '{name}' not found.")
        return

    entry = entries[name]

    print()
    print(f"=== Edit: {name} ===")
    print("Press Enter to keep the current value.")
    print()

    username = input(
        f"Username [{entry.get('username', '')}]: "
    )

    url = input(
        f"URL [{entry.get('url', '')}]: "
    )

    notes = input(
        f"Notes [{entry.get('notes', '')}]: "
    )

    change_password = input(
        "Change password? (y/N): "
    ).lower()

    if username:
        entry["username"] = username

    if url:
        entry["url"] = url

    if notes:
        entry["notes"] = notes

    if change_password == "y":
        new_password = getpass.getpass(
            "New password: "
        )

        entry["password"] = new_password

    if save_vault(data):
        print()
        print(f"✓ Password '{name}' updated.")


# ============================================================
# DELETE PASSWORD
# ============================================================

def delete_password(name):

    if not name:
        print("Usage: password delete <name>")
        return

    data = unlock_vault()

    if data is None:
        return

    entries = data.get("entries", {})

    if name not in entries:
        print(f"✗ Entry '{name}' not found.")
        return

    print()
    print(f"WARNING: This will delete '{name}'.")
    confirm = input("Type DELETE to continue: ")

    if confirm != "DELETE":
        print("Delete cancelled.")
        return

    del entries[name]

    if save_vault(data):
        print()
        print(f"✓ Password '{name}' deleted.")


# ============================================================
# GENERATE PASSWORD
# ============================================================

def generate_password():

    print()
    print("=== Secure Password Generator ===")
    print()

    length_input = input(
        "Password length [24]: "
    ).strip()

    if length_input:
        try:
            length = int(length_input)
        except ValueError:
            print("✗ Invalid length.")
            return
    else:
        length = 24

    if length < 8:
        print("✗ Password length must be at least 8.")
        return

    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    print()
    print("Generated password:")
    print()
    print(password)
    print()


# ============================================================
# RESET VAULT
# ============================================================

def reset_vault():

    if not vault_exists():
        print("No vault exists.")
        return

    print()
    print("======================================")
    print("WARNING: VAULT RESET")
    print("======================================")
    print()
    print("This will permanently delete your")
    print("entire password vault.")
    print()
    print("ALL saved:")
    print("  • passwords")
    print("  • usernames")
    print("  • URLs")
    print("  • notes")
    print()
    print("will be permanently destroyed.")
    print()
    print("This cannot be undone.")
    print()

    confirm = input(
        "Type RESET to continue: "
    )

    if confirm != "RESET":
        print()
        print("Vault reset cancelled.")
        return

    master = getpass.getpass(
        "Enter your master password: "
    )

    try:
        with open(VAULT_FILE, "r") as f:
            vault = json.load(f)

        salt = base64.b64decode(
            vault["salt"]
        )

        nonce = base64.b64decode(
            vault["nonce"]
        )

        encrypted = base64.b64decode(
            vault["data"]
        )

        key = derive_key(
            master,
            salt
        )

        aes = AESGCM(key)

        # Verify password before deleting vault
        aes.decrypt(
            nonce,
            encrypted,
            None
        )

    except Exception:
        print()
        print("✗ Incorrect master password.")
        print("Vault was NOT deleted.")
        return

    try:
        os.remove(VAULT_FILE)

        print()
        print("✓ Vault permanently deleted.")
        print()
        print("Run 'password init' to create a new vault.")

    except Exception as e:
        print()
        print("✗ Could not delete vault.")
        print(e)


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) < 2:
        help_command()
        return

    command = sys.argv[1].lower()

    # -------------------------
    # INIT
    # -------------------------

    if command == "init":
        create_vault()

    # -------------------------
    # ADD
    # -------------------------

    elif command == "add":

        if len(sys.argv) < 3:
            print("Usage: password add <name>")
            return

        name = " ".join(sys.argv[2:])

        add_password(name)

    # -------------------------
    # LIST
    # -------------------------

    elif command == "list":
        list_passwords()

    # -------------------------
    # SHOW
    # -------------------------

    elif command == "show":

        if len(sys.argv) < 3:
            print("Usage: password show <name>")
            return

        name = " ".join(sys.argv[2:])

        show_password(name)

    # -------------------------
    # EDIT
    # -------------------------

    elif command == "edit":

        if len(sys.argv) < 3:
            print("Usage: password edit <name>")
            return

        name = " ".join(sys.argv[2:])

        edit_password(name)

    # -------------------------
    # DELETE
    # -------------------------

    elif command == "delete":

        if len(sys.argv) < 3:
            print("Usage: password delete <name>")
            return

        name = " ".join(sys.argv[2:])

        delete_password(name)

    # -------------------------
    # GENERATE
    # -------------------------

    elif command == "generate":
        generate_password()

    # -------------------------
    # RESET
    # -------------------------

    elif command == "reset":
        reset_vault()

    # -------------------------
    # HELP
    # -------------------------

    elif command in ("help", "-h", "--help"):
        help_command()

    # -------------------------
    # UNKNOWN
    # -------------------------

    else:
        print(f"Unknown command: {command}")
        print()
        help_command()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
