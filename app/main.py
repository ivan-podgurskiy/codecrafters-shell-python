import sys


def main():
    while True:
        sys.stdout.write("$ ")
        
        # Wait for user input
        whole_input = input()

        # split first word and rest from the input
        command, args = (whole_input.split(" ", maxsplit=1) + [""])[:2]
    
        if command == "exit":
            break
        elif command == "echo":
            print(args)
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
