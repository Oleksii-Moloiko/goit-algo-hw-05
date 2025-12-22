
from typing import Callable


def parse_input(user_input: str):
    parts = user_input.split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    return cmd, args

def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "This contact does not exist."
        except IndexError:
            return "Not enough arguments provided."
    return inner

def args_required(func):
    def  inner(args, *rest):
        if not args:
            return "Enter the argument for the command"
        return func(args, *rest)
    return inner

@input_error
@args_required
def add_contact(args, contacts):
    name, phone = args  # може кинути ValueError якщо args не 2
    contacts[name] = phone
    return "Contact added."

@input_error
@args_required
def change_contact(args, contacts):
    name, phone = args  # ValueError якщо args не 2
    if name in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
@args_required
def show_phone(args, contacts):
    name = args[0]  # IndexError якщо порожньо
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(contacts):
    if not contacts:
        return "Contact list is empty."

    lines = []
    for name, phone in contacts.items():
        lines.append(f"{name}: {phone}")
    return "\n".join(lines)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        if command == "hello":
            print("How can l help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()