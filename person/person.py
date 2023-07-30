
from person.BasePerson import BasePerson as Person
from person.Human import Human
from person.HealthyButWeak import HealthyButWeak
from person.MotivatedButWeak import MotivatedButWeak
from person.SlowButStrong import SlowButStrong

people: list[Person] = [
    Human,
    HealthyButWeak,
    MotivatedButWeak,
    SlowButStrong   
]
