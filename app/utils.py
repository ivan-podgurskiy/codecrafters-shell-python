import os

def find_in_path(path, command):
    paths = path.split(":")
    for path in paths:
        possible_command_path = f"{path}/{command}"

        exists = os.access(possible_command_path, os.F_OK)
        is_executable = os.access(possible_command_path, os.X_OK)

        if exists and is_executable:
            return possible_command_path

    return None