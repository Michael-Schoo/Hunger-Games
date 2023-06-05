
class BasePerson():
    # The default stats for a person
    health = 100
    motivation = 50

    # The min stats for a person (but customizable)
    speed: float = 5
    damage: float = 5
    protection: float = 5

    penalties = {
        'speed': 1,
        'damage': 1,
        'protection': 1,
        'health': 1,
        'motivation': 1
    }

    death_day: int = None

    name: str | None = None

    def __init__(self, speed: float, damage: float, protection: float, ai=True):

        # speed + damage + protection must be equal to 50 and their min is 5 each
        if speed + damage + protection != 50:
            raise Exception('Speed + damage + protection must be equal to 50')

        if speed < 5 or damage < 5 or protection < 5:
            raise Exception('Speed, damage and protection must be at least 5')

        self.speed = speed
        self.damage = damage
        self.protection = protection

        self.ai = ai
        """ Just changes wether to use input or random for the person's actions"""

    def __str__(self):
        return f"<Person: {self.name}>"

    def __repr__(self):
        return self.__str__()

    def alive(self):
        return self.health > 0

    def get_health(self):
        return self.health * self.penalties['health']

    def get_motivation(self):
        return self.motivation * self.penalties['motivation']

    def get_speed(self):
        return self.speed * self.penalties['speed']

    def get_damage(self):
        return self.damage * self.penalties['damage']

    def get_protection(self):
        return self.protection * self.penalties['protection']

    def get_stats(self, raw=False):
        if raw:
            return {
                'health': self.health,
                'motivation': self.motivation,
                'speed': self.speed,
                'damage': self.damage,
                'protection': self.protection
            }

        return {
            'health': self.get_health(),
            'motivation': self.get_motivation(),
            'speed': self.get_speed(),
            'damage': self.get_damage(),
            'protection': self.get_protection()
        }

    def remove_health(self, amount: float):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def remove_motivation(self, amount: float):
        self.motivation -= amount
        if self.motivation < 0:
            self.motivation = 0

    def add_health(self, amount: float):
        if self.health == 0:
            return

        self.health += amount
        if self.health > 150:
            self.health = 150

    def add_motivation(self, amount: float):
        self.motivation += amount
        if self.motivation > 100:
            self.motivation = 100

    def deal_damage(self, amount: float):
        self.remove_health(amount)

    # the day choices are used for the player to choose what to do each day
    # it is stored here to be accessed easily in the fight class
    day_choices = {}

    def get_day_choice(self, day: int) -> str:
        return self.day_choices[day]

    def set_day_choice(self, day: int, choice: str):
        self.day_choices[day] = choice
