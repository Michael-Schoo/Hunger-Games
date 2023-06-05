import random
from fight import Fight
from person.BasePerson import BasePerson as Person
import asyncio
import concurrent.futures

from stats import Stats

"""
The day class makes the matches of the people to fight (or not)

At the start of the day, people can run away or fight:
    - If they run away, they have a less chance of attack and lose motivation
        - higher speed = higher chance of running away
    - If they fight, they have a higher chance of attack and gain motivation

The choices happen first, and then matches are made
"""

class Day():
    def __init__(self, stats: Stats, people: list[Person], game_data: dict[{'game': int, 'iteration': int, 'day': int}]):
        self.people = people
        """ The people that will fight today """

        self.game_data = game_data
        self.stats = stats

        self.matches = []
        """ The matches that will happen today """

        self.games = []

    def run(self):
        """
        Runs the day
        """

        # Get the choices of the people
        for person in self.people:
            choice = self.get_choice(person)
            person.set_day_choice(self.game_data['day'], choice)

            # at the start of the day, add health
            person.add_health(5)

        # Make the matches
        self.make_matches()

        # Run the matches
        self.run_matches()

        # Return the matches
        return self.matches

    def get_choice(self, person: Person):
        """
        Gets the choice of a person
        """

        choices = ['fight', 'run']

        if person.ai:
            return random.choice(choices)
        else:
            return input(f'What do you want to do? {choices}: ')

    def make_matches(self):
        """
        Makes the matches
        """

        # Make a copy of the people
        people = self.people.copy()

        # Shuffle the people
        random.shuffle(people)

        # Make the matches
        # Go through each people and match them with the next person
        # But have a chance of a person not fighting
        while len(people) > 0:
            person = people.pop(0)
            if self.check_for_run_away(person):
                continue

            person2 = None
            while person2 == None:
                try:
                    person2 = people.pop(0)
                except IndexError:
                    break

                if self.check_for_run_away(person2):
                    person2 = None
                    continue

            if person2 != None:
                self.matches.append((person, person2))

    def check_for_run_away(self, person: Person):
        # if they said to run away, see if they have good chances
        if person.get_day_choice(self.game_data['day']) == 'run':
            if self.run_away_chance(person):
                person.add_motivation(10)
                return True
            else:
                person.remove_motivation(5)
        # otherwise, they said to fight, so add them to the matches and give them motivation
        else:
            person.add_motivation(5)

        return False

    def run_matches(self):
        """
        Runs the matches
        """

        for id, match in enumerate(self.matches):
            fight = Fight(self.stats, match[0], match[1], game_data={**self.game_data, 'fight_num': id})
            self.games.append(fight)
            fight.run()


    def run_away_chance(self, person: Person) -> bool:
        """
        Returns if the person ran away or not
        """

        return random.randint(0, 35) < person.speed
