#!/usr/bin/env python3

import sys
import os

NOTES_DIR = os.path.expanduser("~/.tnv/notes")
os.makedirs(NOTES_DIR, exist_ok=True)


def help_note():
    print("""
NOTE - Terminal Notes

Usage:
  note add "title"
  note list
  note show <id>
  note search "query"
  note edit <id>
  note delete <id>
""")


def get_notes():
    notes = []

    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            try:
                notes.append(int(filename[:-4]))
            except ValueError:
                pass

    return sorted(notes)


def add_note(title):
    notes = get_notes()
    note_id = max(notes, default=0) + 1

    print("Write your note.")
    print("Type . on a new line to finish.\n")

    lines = []

    while True:
        line = input()

        if line == ".":
            break

        lines.append(line)

    with open(
        os.path.join(NOTES_DIR, f"{note_id}.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(f"TITLE={title}\n\n")
        f.write("\n".join(lines))

    print(f"Note {note_id} created.")


def list_notes():
    notes = get_notes()

    if not notes:
        print("No notes.")
        return

    for note_id in notes:
        path = os.path.join(NOTES_DIR, f"{note_id}.txt")

        with open(path, encoding="utf-8") as f:
            first_line = f.readline().strip()

        title = first_line.replace("TITLE=", "")

        print(f"{note_id}: {title}")


def show_note(note_id):
    path = os.path.join(NOTES_DIR, f"{note_id}.txt")

    if not os.path.exists(path):
        print(f"Note {note_id} does not exist.")
        return

    with open(path, encoding="utf-8") as f:
        print(f.read())


def search_notes(query):
    found = False

    for note_id in get_notes():
        path = os.path.join(NOTES_DIR, f"{note_id}.txt")

        with open(path, encoding="utf-8") as f:
            content = f.read()

        if query.lower() in content.lower():
            title = content.splitlines()[0].replace("TITLE=", "")
            print(f"{note_id}: {title}")
            found = True

    if not found:
        print("No matching notes.")


def delete_note(note_id):
    path = os.path.join(NOTES_DIR, f"{note_id}.txt")

    if not os.path.exists(path):
        print(f"Note {note_id} does not exist.")
        return

    os.remove(path)
    print(f"Note {note_id} deleted.")


def note_command(args):

    if not args or args[0] in ("help", "--help", "-h"):
        help_note()
        return

    action = args[0]

    if action == "add":

        if len(args) < 2:
            print('Usage: note add "title"')
            return

        add_note(" ".join(args[1:]))

    elif action == "list":

        list_notes()

    elif action == "show":

        if len(args) != 2:
            print("Usage: note show <id>")
            return

        show_note(args[1])

    elif action == "search":

        if len(args) < 2:
            print('Usage: note search "query"')
            return

        search_notes(" ".join(args[1:]))

    elif action == "delete":

        if len(args) != 2:
            print("Usage: note delete <id>")
            return

        delete_note(args[1])

    else:
        print(f"Unknown note command: {action}")
        print("Run 'note help'.")


def main():

    # This lets us know whether the program was launched as
    # "note" or "password".

    command = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if command == "note":
        note_command(args)

    else:
        print("Unknown command.")
        print("Use: note")


if __name__ == "__main__":
    main()
