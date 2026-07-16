import os
import sys
import readline

from app.constants import BUILTIN_COMMANDS


def make_completer(path):
    tab_count = 0
    last_text = None

    def completer(text, state):
        nonlocal tab_count, last_text

        if state != 0:
            return None

        if text != last_text:
            tab_count = 0
            last_text = text

        matches = sorted(autocompleter(text, path))
        if not matches:
            return None

        if len(matches) == 1:
            tab_count = 0
            return matches[0] + " "

        prefix = os.path.commonprefix(matches)
        if prefix != text:
            tab_count = 0
            return prefix

        tab_count += 1
        if tab_count == 1:
            sys.stdout.write("\x07")
            sys.stdout.flush()
            return None

        sys.stdout.write("\n" + "  ".join(matches) + "\n$ " + readline.get_line_buffer())
        sys.stdout.flush()
        tab_count = 0
        return None

    return completer


def find_in_path(path, command, partial=False):
    directories = path.split(":")

    if partial:
        matches = []
        seen = set()
        for directory in directories:
            try:
                names = os.listdir(directory)
            except OSError:
                continue
            for name in names:
                if not name.startswith(command) or name in seen:
                    continue
                full = f"{directory}/{name}"
                if os.access(full, os.X_OK) and not os.path.isdir(full):
                    matches.append(name)
                    seen.add(name)
        return matches

    for directory in directories:
        possible_command_path = f"{directory}/{command}"
        exists = os.access(possible_command_path, os.F_OK)
        is_executable = os.access(possible_command_path, os.X_OK)
        if exists and is_executable:
            return possible_command_path

    return None


def autocompleter(text, path):
    builtin_commands = autocomplete_builtin_commands(text)
    if builtin_commands:
        return builtin_commands
    return find_in_path(path, text, partial=True)


def autocomplete_builtin_commands(text):
    return [c for c in BUILTIN_COMMANDS if c.startswith(text)]
