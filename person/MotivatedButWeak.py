
from person.BasePerson import BasePerson as Person


class MotivatedButWeak(Person):
    def __init__(self, speed, damage, protection):
        super().__init__(speed, damage, protection)

    penalties = {
        'speed': 1,
        'damage': 0.5,
        'protection': 0.5,
        'health': 1,
        'motivation': 2
    }
