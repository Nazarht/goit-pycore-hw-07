import readline
import traceback

from utils import parse_input
from handlers import handlers
from states import AddressBook

def main():
    contacts = AddressBook()

    while True:
        try:
            user_input = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        if not user_input.strip():
            continue

        command, args = parse_input(user_input)
        command = command.lower()

        if command in ("exit", "close"):
            print("Good bye!")
            break

        handler = handlers.get(command, None)
        if handler is None:
            print("Invalid command")
            continue

        result = handler(args, contacts)
        print(result)


if __name__ == "__main__":
    main()
