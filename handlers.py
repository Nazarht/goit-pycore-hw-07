from collections import defaultdict

from decorators import input_error
from states import AddressBook


def hello(_: list[str], __: AddressBook) -> None:
    return "How can I help you?"


@input_error
def add_contact(args: list[str], contacts: AddressBook) -> str:
    contact_name, contact_phone_number = args
    record = contacts.find(contact_name)
    if record is None:
        record = contacts.add_record(contact_name)

    record.add_phone(contact_phone_number)
    return f"Contact {contact_name} added successfully"


@input_error
def change_phone(args: list[str], contacts: AddressBook) -> str:
    contact_name, old_phone_number, new_phone_number = args

    contacts.find(contact_name).edit_phone(old_phone_number, new_phone_number)
    return f"Contact {contact_name} updated successfully"


@input_error
def get_phone(args: list[str], contacts: AddressBook) -> str:
    contact_name = args[0]

    return f"Contact {contact_name} phone number{'' if len(contacts.find(contact_name).phones) == 1 else 's'} are: {', '.join(phone.value for phone in contacts.find(contact_name).phones)}"


@input_error
def get_all(_: list[str], contacts: AddressBook) -> str:
    result: list[str] = []

    for contact_name, contact_phone_number in contacts.data.items():
        result.append(
            f"{contact_name} - {', '.join(phone.value for phone in contact_phone_number.phones)}{(' - Birthday: ' + contact_phone_number.birthday.value.strftime('%d.%m.%Y')) if contact_phone_number.birthday else ''}")

    if not result:
        return "No contacts found"

    return "\n".join(result)


@input_error
def add_birthday(args: list[str], contacts: AddressBook) -> str:
    contact_name, contact_birthday = args
    contacts.find(contact_name).add_birthday(contact_birthday)
    return f"Birthday {contact_birthday} added successfully"


@input_error
def show_birthday(args: list[str], contacts: AddressBook) -> str:
    contact_name = args[0]
    return f"Birthday {contacts.find(contact_name).birthday.value}"


@input_error
def birthdays(args: list[str], contacts: AddressBook) -> str:
    upcoming_birthdays = contacts.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays"
    return "\n".join(f"{birthday['name']} needs to be congratulated on {birthday['congratulation_date']}" for birthday in upcoming_birthdays)


handlers: dict[str, callable] = {
    "hello": hello,
    "add": add_contact,
    "change": change_phone,
    "phone": get_phone,
    "all": get_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}
