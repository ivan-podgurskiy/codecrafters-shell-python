import sys
import os

available_commands = ["type", "echo", "exit"]


def find_in_path(path, command):
    paths = path.split(":")
    for path in paths:
        possible_command_path = f"{path}/{command}"

        exists = os.access(possible_command_path, os.F_OK)
        is_executable = os.access(possible_command_path, os.X_OK)

        if exists and is_executable:
            return possible_command_path

    return None


def main():
    path = os.environ["PATH"]
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        whole_input = input()

        # split first word and rest from the input
        command, args = (whole_input.split(" ", maxsplit=1) + [""])[:2]

        if command in available_commands:
            match command:
                case "type":
                    if args in available_commands:
                        print(f"{args} is a shell builtin")
                    elif found_path := find_in_path(path, args):
                        print(f"{args} is {found_path}")
                    else:
                        print(f"{args}: not found")
                case "echo":
                    print(args)
                case "exit":
                    break
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
