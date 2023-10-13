from collections import UserDict


class PhoneError(Exception):
    ...


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    # def __repr__(self) -> str:
    #     return str(self)


class Name(Field):
    ...


class Phone(Field):

    def __init__(self, value):
        if len(value) == 10 and int(value):
            self.value = phone
            super().__init__(value)
        else:
            raise ValueError


class Record:

    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                self.phones[idx] = new_phone
                return f"Phone {old_phone} changed to phone {new_phone}"

    def find_phone(self, phone):
        for p in self.phones:
            if phone.value == p.value:
                return phone
        raise PhoneError

    def remove_phone(self, phone):
        if phone.value in self.phones:
            self.phones.remove(phone)
        else:
            raise PhoneError

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record):
        rec = self.data.get(record.name.value)
        if rec:
            f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in rec)}"
            return rec
        else:
            raise KeyError

    def delete(self, record):
        if self.data.get(record.name.value):
            del self.data[record.name.value]
        else:
            raise KeyError


customers = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. It needs to have 2 params (Name Phone): "
        except KeyError:
            return "This name doesn't have in the dictionary."
        except NameError:
            return "This name is already in the dictionary. Use 'add phone' to append new phone."
        except ValueError:
            return "The phone number must contains only 10 digit."
        except PhoneError:
            return "This phone number doesn't exist in the dictionary."
    return inner


@input_error
def add_record(*args):
    name = Name(args[0].lower())
    phone = Phone(args[1])
    rec = customers.get(name.value)
    if rec:
        raise NameError
    rec = Record(name, phone)
    customers.add_record(rec)
    return f"Add name = {name}, phone = {phone}"


@input_error
def change_record(*args):
    name = Name(args[0].lower())
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = customers.get(name.value)
    if rec:
        print(f"{args[0].capitalize()}'s phone {args[1]} changed to {args[2]}")
        return rec.edit_phone(old_phone, new_phone)
    else:
        raise KeyError


@input_error
def find_record(*args):
    name = Name(args[0].lower())
    rec = customers.get(name.value)
    if rec:
        return rec
    else:
        raise KeyError


@input_error
def del_record(*args):
    name = Name(args[0].lower())
    rec = customers.get(name.value)
    if rec:
        customers.delete(rec)
        return f"Record with name {args[0].capitalize()} deleted."
    else:
        raise KeyError


@input_error
def add_phone(*args):
    name = Name(args[0].lower())
    new_phone = Phone(args[1])
    rec = customers.get(name.value)
    if rec:
        rec.add_phone(new_phone)
        return f"{args[0].capitalize()}'s phone added another one {args[1]}"
    else:
        raise KeyError


@input_error
def find_phone(*args):
    name = Name(args[0].lower())
    phone = Phone(args[1])
    rec = customers.get(name.value)
    if rec:
        find_phone = rec.find_phone(phone)
        return f'{name.value} : {find_phone}'
    else:
        raise PhoneError


@input_error
def remove_phone(*args):
    name = Name(args[0].lower())
    phone = Phone(args[1])
    rec = customers.get(name.value)
    if rec:
        rec.remove_phone(phone)
        return f'{phone.value} deleted.'
    else:
        raise PhoneError


def unknown(*args):
    return "Unknown command. Try again."


def end_program(*args):
    return "Good Bye!"


def hello(*args):
    return "How can I help you?:"


def help(*args):
    message = '''Use next commands:
    add 'name' 'phone'  - add name and phone number to the dictionary
    append 'name' 'phone'  - add phone number to the name in dictionary
    change 'name' 'old_phone' 'new_phone' - change phone number in this name
    delete 'name' - delete name and phones from the dictionary
    find 'name' - find info by name
    seek 'name' 'phone' - find phone for name in the dictionary
    phone 'name' - show phone number for this name
    remove phone 'name' 'phone' - remove phone for this name
    show all  -  show all records in memory
    exit - exit from bot'''
    return message


def show_all(*args):
    for name, record in customers.data.items():
        print(record)
    return "There is all records in dictionary"


@input_error
def phone(*args):
    name = args[0].lower()
    if customers[name]:
        return f'{name.capitalize()} has {customers[name]} phone number.'


COMMANDS = {add_record: "add",
            add_phone: "add_phone",
            change_record: "change",
            del_record: "delete",
            end_program: "exit",
            find_record: "find",
            find_phone: 'seek',
            hello: "hello",
            help: "help",
            phone: "phone",
            show_all: "show all",
            remove_phone: "remove phone"
            }


def parser(text: str):
    for func, kw in COMMANDS.items():
        command = text.rstrip().split()
        print(command[0], kw)
        if kw == command[0].lower:
            return func, text[len(kw):].strip().split()
        # if text.lower().startswith(kw):
        #     return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(
            "Enter user name and phone number or 'help' for help: ")
        func, data = parser(user_input)
        print(func(*data))
        if user_input == 'exit':
            break


if __name__ == '__main__':
    main()
