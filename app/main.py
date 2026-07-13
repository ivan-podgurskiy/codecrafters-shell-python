import sys
import os
import subprocess
from contextlib import ExitStack

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
        command, args, stdout_file, stderr_file = parse_input(whole_input, home)

        if command in BUILTIN_COMMANDS:
            match command:
                case "type":
                    cmd_type(args, path)
                case "pwd":
                    cmd_pwd(args)
                case "cd":
                    cmd_cd(args, home)
                case "echo":
                    with ExitStack() as stack:
                        if stderr_file:
                            stack.enter_context(open(stderr_file, "w"))
                        if stdout_file:
                            cmd_echo(args, out=stack.enter_context(open(stdout_file, "w")))
                        else:
                            cmd_echo(args)
                case "exit":
                    break
        elif find_in_path(path, command):
            with ExitStack() as stack:
                kwargs = {}
                if stdout_file:
                    kwargs["stdout"] = stack.enter_context(open(stdout_file, "w"))
                if stderr_file:
                    kwargs["stderr"] = stack.enter_context(open(stderr_file, "w"))
                subprocess.run([command, *args], **kwargs)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
