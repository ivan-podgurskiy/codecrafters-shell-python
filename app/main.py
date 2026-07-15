import sys
import os
import subprocess
import readline
from contextlib import ExitStack

from .constants import BUILTIN_COMMANDS

from .utils import autocompleter, find_in_path
from .builtins import cmd_echo, cmd_pwd, cmd_type, cmd_cd
from .parser import parse_input


def main():
    path = os.environ["PATH"]
    home = os.getenv("HOME")
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

        tab_count += 1
        if tab_count == 1:
            sys.stdout.write("\x07")
            sys.stdout.flush()
            return None

        sys.stdout.write("\n" + "  ".join(matches) + "\n$ " + readline.get_line_buffer())
        sys.stdout.flush()
        tab_count = 0
        return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        whole_input = input()

        # split first word and rest from the input
        command, args, stdout_file, stderr_file, stdout_append, stderr_append = (
            parse_input(whole_input, home)
        )

        if not command:
            continue

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
                            stack.enter_context(
                                open(stderr_file, "w" if not stderr_append else "a")
                            )
                        if stdout_file:
                            cmd_echo(
                                args,
                                out=stack.enter_context(
                                    open(stdout_file, "w" if not stdout_append else "a")
                                ),
                            )
                        else:
                            cmd_echo(args)
                case "exit":
                    break
        elif find_in_path(path, command):
            with ExitStack() as stack:
                kwargs = {}
                if stdout_file:
                    kwargs["stdout"] = stack.enter_context(
                        open(stdout_file, "w" if not stdout_append else "a")
                    )
                if stderr_file:
                    kwargs["stderr"] = stack.enter_context(
                        open(stderr_file, "w" if not stderr_append else "a")
                    )
                subprocess.run([command, *args], **kwargs)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
