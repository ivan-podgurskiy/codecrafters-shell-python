import sys

available_commands = ["type", "echo", "exit"]


def main():
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
