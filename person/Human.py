
from person.BasePerson import BasePerson as Person


class Human(Person):
    def __init__(self, speed, damage, protection):
        super().__init__(speed, damage, protection)

