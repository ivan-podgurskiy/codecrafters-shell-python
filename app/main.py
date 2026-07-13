import sys
import os
import subprocess

from .utils import find_in_path
from .builtins import cmd_echo, cmd_pwd, cmd_type, cmd_cd
from .constants import BUILTIN_COMMANDS
from .parser import parse_input


def main():
    path = os.environ["PATH"]
    home = os.getenv("HOME")

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        whole_input = input()

        # split first word and rest from the input
        command, args, stdout_file = parse_input(whole_input, home)

        if command in BUILTIN_COMMANDS:
            match command:
                case "type":
                    cmd_type(args, path)
                case "pwd":
                    cmd_pwd(args)
                case "cd":
                    cmd_cd(args, home)
                case "echo":
                    if stdout_file:
                        with open(stdout_file, "w") as f:
                            cmd_echo(args, out=f)
                    else:
                        cmd_echo(args)
                case "exit":
                    break
        elif find_in_path(path, command):
            if stdout_file:
                with open(stdout_file, "w") as f:
                    subprocess.run([command, *args], stdout=f)
            else:
                subprocess.run([command, *args])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
