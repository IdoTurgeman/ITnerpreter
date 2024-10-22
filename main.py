import sys
from Tokenizer import TokenizationProcess
from Parser import ParsingProcess

# ============ main program ==============
PROGRAM_ERROR = 1

def main():
    if len(sys.argv) < 3:
        print("Usage: ./main.py <command> <filename>", file=sys.stderr)
        print("possible commands: [tokenize, parse]")
        return PROGRAM_ERROR

    command = sys.argv[1]
    filename = sys.argv[2]
    try:
        with open(filename) as file:
            file_content = file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return PROGRAM_ERROR

    if command == "tokenize":
        return TokenizationProcess(file_content=file_content)
    elif command == "parse":
        return ParsingProcess(file_content=file_content)

    print(f"Unknown command: {command}", file=sys.stderr)
    return PROGRAM_ERROR


if __name__ == "__main__":
    main()
