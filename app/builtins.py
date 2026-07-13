import sys
import os

from .constants import BUILTIN_COMMANDS
from .utils import find_in_path

def cmd_echo(args, out=sys.stdout):
    print(*args, file=out)

def cmd_pwd(_):
    print(os.getcwd())

def cmd_type(args, path):
    name = args[0] if args else ""

    if name in BUILTIN_COMMANDS:
        print(f"{name} is a shell builtin")
    elif found_path := find_in_path(path, name):
        print(f"{name} is {found_path}")
    else:
        print(f"{name}: not found")


def cmd_cd(args, home):
    if not args:
        os.chdir(home)
        return

    dir = args[0]

    if os.path.isdir(dir):
        os.chdir(dir)
    else:
        print(f"cd: {dir}: No such file or directory")