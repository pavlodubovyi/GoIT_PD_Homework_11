from collections import UserDict
from collections.abc import Iterator
from datetime import datetime

class Field:
    def __init__(self, value) -> None:
        self.value = value

    
class Phone(Field):
    @property
    def value(self):
        return self.something
    
    @value.setter
    def value(self, new_value):
        try:
            if not isinstance(new_value, str) or not new_value.isdigit() or len(new_value) != 10:
                raise ValueError
            self.something = new_value
        except ValueError:
            print(f"The phone number {new_value} is invalid. Phone number must have 10 digits")
            self.something = None


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

        try:
            self.some_value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Wrong birthday format. Enter 'DD-MM-YYYY'")

    @property
    def value(self):
        return self.some_value
    
    @value.setter
    def value(self, new_value):
        self.some_value = new_value


class Record:
    def __init__(self, name: Name, *phones: Phone, birthday: Birthday=None, **kwargs) -> None:
        self.name = name
        self.phones = list()
        if phones:
            for num in phones:
                self.phones.append(num)
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
        next_birthday = self.birthday.value.replace(year=current_date.year)
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

    # далі починаються мої перевірочні тести
    name_1 = Name('Bill')
    phone_1 = Phone('1234567890')
    phone_2 = Phone('098')
    birthday_1 = Birthday("19-06-2004")
    rec_1 = Record(name_1, phone_1, phone_2, birthday=birthday_1, )
    ab = AddressBook()
    ab.add_record(rec_1)
  
    name_2 = Name('Joe')
    birthday_2 = Birthday("23-11-1984")
    rec_2 = Record(name_2, birthday=birthday_2)
    ab.add_record(rec_2)

    name_3 = Name('Witney')
    birthday_3 = Birthday("21-01-1985")
    phone_Witney_1 = Phone('0987654321')
    phone_Witney_2 = Phone('7654')
    rec_3 = Record(name_3, phone_Witney_1, phone_Witney_2, birthday=birthday_3)
    ab.add_record(rec_3)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    assert isinstance(ab['Joe'], Record)
    assert isinstance(ab['Joe'].name, Name)
    assert isinstance(ab['Joe'].phones, list)

    if ab['Joe'].phones:
        assert isinstance(ab['Joe'].phones[0], Phone)
        assert ab['Joe'].phones[0].value is None

    for record_piece in ab.iterator(piece_size=2):
        for contact in record_piece:
            print(f"Name: {contact.name.value}")
            if contact.birthday:
                birthday_formatted = contact.birthday.value.strftime('%d-%m-%Y')
                print(f"Birthday on: {birthday_formatted}, days to birthday: {contact.days_to_birthday()}")
            if contact.phones:
                valid_phones = [phone.value for phone in contact.phones if phone.value is not None]
                print(f"Phones: {', '.join(valid_phones)}")
            print('-' * 20)

