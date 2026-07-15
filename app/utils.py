import os

from app.constants import BUILTIN_COMMANDS


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
