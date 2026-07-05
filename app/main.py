import sys
import os
import subprocess
import shlex

available_commands = ["pwd", "cd", "type", "echo", "exit"]


def find_in_path(path, command):
    paths = path.split(":")
    for path in paths:
        possible_command_path = f"{path}/{command}"

        exists = os.access(possible_command_path, os.F_OK)
        is_executable = os.access(possible_command_path, os.X_OK)

        if exists and is_executable:
            return possible_command_path

    return None

def parse_input(line):
    parts = shlex.split(line)

    if not parts:
        return "", []

    return parts[0], parts[1:]

def main():
    path = os.environ["PATH"]
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        whole_input = input()

        # split first word and rest from the input
        command, args = parse_input(whole_input)

        if command in available_commands:
            name =  args[0] if args else ""
            match command:
                case "type":
                    if name in available_commands:
                        print(f"{name} is a shell builtin")
                    elif found_path := find_in_path(path, name):
                        print(f"{name} is {found_path}")
                    else:
                        print(f"{name}: not found")
                case "pwd":
                    print(os.getcwd())
                case "cd":
                    # Check if args is directory and it exist
                    # We probably need a proper sanitation here.

                    # Let's consider ~ too
                    dir = (
                        args.replace("~", os.getenv("HOME"))
                        if args.startswith("~")
                        else args
                    )

                    if os.path.isdir(dir):
                        os.chdir(dir)
                    else:
                        print(f"cd: {dir}: No such file or directory")
                case "echo":
                    print(args)
                case "exit":
                    break
        elif find_in_path(path, command):
            subprocess.run([command, *args])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
