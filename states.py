from datetime import datetime, timedelta
from collections import UserDict

from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        
        super().__init__(value)
        
class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(parsed_birthday)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            phone.value = Phone(new_phone).value
            return True
        return False

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
            return True
        return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        new_record = Record(record)
        self.data[record] = new_record
        return new_record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.data.values():
            user_birthday = record.birthday.value
            
            # if birthday is today or in the next 7 days, return the birthday of the current year
            # else return the birthday of the next year
            closest_birthday = \
                user_birthday.replace(year=today.year) \
                if today - user_birthday.replace(year=today.year) <= timedelta(days=7) and user_birthday.replace(year=today.year) > today\
                else user_birthday.replace(year=today.year + 1)
    
            # check if the closest birthday is in the next 7 days
            if (
                closest_birthday - today <= timedelta(days=7)
            ):
                if closest_birthday.weekday() >= 5:
                    closest_birthday += timedelta(
                        days=(2 if closest_birthday.weekday() == 5 else 1)
                    )
    
                upcoming_birthdays.append(
                    (record.name.value, closest_birthday.strftime("%Y.%m.%d"))
                )

        return [{"name": name, "congratulation_date": birthday} for name, birthday in upcoming_birthdays]
