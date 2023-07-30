
from person.BasePerson import BasePerson as Person


class SlowButStrong(Person):
    def __init__(self, speed, damage, protection):
        super().__init__(speed, damage, protection)

    penalties = {
        'speed': 0.5,
        'damage': 1.5,
        'protection': 1,
        'health': 1,
        'motivation': 1
    }
