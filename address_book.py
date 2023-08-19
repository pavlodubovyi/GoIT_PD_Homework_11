from collections import UserDict
from collections.abc import Iterator
from datetime import datetime

class Field:
    def __init__(self, value) -> None:
        self.something = value

    @property
    def value(self):
        return self.something
    
    @value.setter
    def value(self, new_value):
        self.something = new_value
    
class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str) or not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Phone number must have 10 digits")
        self.something = new_value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

        try:
            self._value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Wrong birthday format. Enter 'DD-MM-YYYY'")

    @property
    def value(self):
        return self._value

class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None) -> None:
        self.name = name
        self.phones = list()
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
    
    def add_phone(self, number: Phone):
        phone_number = Phone(number)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def update_phone(self, old_number, new_number):
        index = self.phones.index(old_number)
        self.phones[index] = new_number

    def delete_phone(self, value):
        for num in self.phones:
            if num == value:
                self.phones.remove(value)
    
    def days_to_birthday(self):
        
        current_date = datetime.now()
        next_birthday = birthday.value.replace(year=current_date.year)
        if current_date.date() == next_birthday.date():
            return f"Today's {self.name.value}'s birthday!"
        elif current_date.date() > next_birthday.date():
            next_birthday = next_birthday.replace(year=current_date.year + 1)
        days_left = (next_birthday - current_date).days
        return days_left


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)
    
    def __iter__(self) -> Iterator:
        return self.iterator
    
    def iterator(self, piece_size=5):
        entries = list(self.data.values())
        for i in range(0, len(entries), piece_size):
            yield entries[i:i + piece_size]
    

if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday("19-06-2004")
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
  
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print(ab['Bill'].days_to_birthday())
    
    for record_piece in ab.iterator(piece_size=1):
        for contact in record_piece:
            print(f"Name: {contact.name.value}")
            if contact.birthday:
                birthday_formatted = contact.birthday.value.strftime('%d-%m-%Y')
                print(f"Birthday: {birthday_formatted}")
            if contact.phones:
                print(f"Phones: {', '.join(phone.value for phone in contact.phones)}")
            print('-' * 20)

    print('All Ok)')

"""
 """