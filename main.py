import sys
from Processes import tokenization, parsing, interpreting

PROGRAM_ERROR = 1

def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <filename> [optional] <command>", file=sys.stderr)
        print("possible commands: [tokenize, parse, execute]")
        return PROGRAM_ERROR

    filename = sys.argv[1]
    if len(sys.argv) > 2:
        command = sys.argv[2]
    else:
        command = "execute"

    try:
        with open(filename) as file:
            file_content = file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return PROGRAM_ERROR

    if command == "tokenize":
        return tokenization(file_content=file_content)
    elif command == "parse":
        return parsing(file_content=file_content)
    elif command == "execute":
        return interpreting(file_content=file_content)

    print(f"Unknown command: {command}", file=sys.stderr)
    return PROGRAM_ERROR


if __name__ == "__main__":
    main()
