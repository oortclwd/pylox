import sys

from src.lexer.scanner import Scanner


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)


def run_file(path: str):
    with open(path) as f:
        run(f.read())


def run_prompt():
    while True:
        try:
            line = input("> ")
            run(line)
        except EOFError:
            break
        run(line)


def main(args):
    if len(args) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()


if __name__ == "__main__":
    """
    if no arguments are given, start REPL Mode
    """
    main(sys.argv[1:])
