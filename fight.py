import random
from person.BasePerson import BasePerson as Person
from stats import Stats

"""
Fights work like this (a turn based system):
    1. can choose to
        a. attack
        b. defend
        c. try to run (a chance to work)
    
    2. if attack, then randomize damage
    
    2. if defend, then also randomize damage but less and a higher protection

    2. if run, then randomize a chance to work
        a. if it works, then the fight is over
        b. if it doesn't work, then the fight continues
        c. looses motivation if doesn't work

    3. all protection does is reduce damage, not increase health

    4. if the damage that a player was lower then they did, they get motivation (and vice versa)

"""


class Fight():
    """
    The fight class is responsible for running the fight between two people 
    """

    def __init__(self, stats: Stats, person1: Person, person2: Person, game_data: dict[{'game': int, 'iteration': int, 'day': int, 'fight_num': int}]):
        self.person1 = person1
        self.person2 = person2
        self.game_data = game_data
        self.stats = stats

        self.winner = None
        """ The winner of the fight - can be either None, (person1), (person2), or (person1, person2) """
        self.looser = None

    def run(self):
        """
        Runs the fight
        """

        turn_count = 0
        while self.winner == None:
            turn_count += 1
            d1 = self.turn(self.person1, self.person2)
            d2 = self.turn(self.person2, self.person1)

            # add/remove motivation (depending on outcome of damage dealt)
            if d1 > d2:
                self.person1.add_motivation(5)
                self.person2.remove_motivation(5)
            elif d2 > d1:
                self.person2.add_motivation(5)
                self.person1.remove_motivation(5)
            else:
                self.person1.add_motivation(2)
                self.person2.add_motivation(2)

        # save the data
        if self.game_data:
            self.stats.add_fight(
                self.game_data,
                self.winner,
                self.looser,
                turn_count
            )
        return self.winner

    def get_choice(self, person: Person):
        """
        Gets the choice of a person
        """

        choices = ['attack', 'defend', 'run']

        # use random if player is ai
        if person.ai:
            return random.choice(choices)
        else:
            return input(f'What do you want to do? {choices}: ')

    def get_stats(self, person: Person, choice: str):
        """
        Gets the stats of a person with the defense or attack bonus
        """

        stats = person.get_stats()

        if choice == 'attack':
            stats['damage'] += 5
        elif choice == 'defend':
            stats['protection'] += 5

        return stats

    def run_away_chance(self, person: Person) -> bool:
        """
        Gets the chance of a person running away
        """

        # Using speed as the chance, so higher speed = higher chance
        return random.randint(0, 500) < person.get_stats()['speed']

    def turn(self, player: Person, opponent: Person) -> int:
        """
        Runs a turn of the fight

        returns the damage done
        """

        if self.winner != None:
            return 0

        # get the choice
        choice = self.get_choice(player)

        # if they want to run away
        if choice == 'run':
            if self.run_away_chance(player):
                self.winner = (player, opponent)
                self.looser = None
                player.add_motivation(10)
                return 0
            else:
                player.remove_motivation(5)

        # get the stats
        stats = self.get_stats(player, choice)

        # get the damage
        damage = random.randint(5, stats['damage']) * (stats['motivation'] / 50)

        # get the protection
        protection = random.randint(5, stats['protection']) * (stats['motivation'] / 50) / 10

        damage_dealt = abs(protection - damage)

        # deal the damage
        opponent.deal_damage(damage_dealt)

        # check if the opponent is dead (if so, set the winner)
        if opponent.get_health() <= 0:
            opponent.death_day = self.game_data['day']
            self.winner = player
            self.looser = opponent

        return damage_dealt
