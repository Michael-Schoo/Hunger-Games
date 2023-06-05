

import csv
from person.BasePerson import BasePerson
from statistics import mean
import os
import json
from json import JSONDecoder

stat = dict[{'specie': str, 'speed': int, 'damage': int, 'protection': int}]


class Stats():
    """
    This should contain all the results of the simulation

    It is then used to inform the next evolution
    """

    fights: list[dict[tuple[int, int, int], dict[{'winner_stat': stat, 'winner_remaining_health': float, 'turns': int}]]] = []
    """"
    ```
    games = [
        fights[(iteration, day, game_num)] = {
            'winner_stat': winner_stats {
                'specie': 'human',
                'speed': 15,
                'damage': 15,
                'protection': 15,
            },
            'winner': <class>,
            'winner_remaining_health': 0.1,
            'turns': 5,
        }
    ]
    ```
    """

    def __init__(self, games: int = 1):
        self.fights = []

        # go through all the games and add a dict for each
        for i in range(games):
            self.fights.append({})

    def add_fight(self, game_data: dict[{'game': int, 'iteration': int, 'day': int, 'fight_num': int}], winner: BasePerson | tuple[BasePerson, BasePerson], loser: BasePerson, turns: int):

        winner_health = 0
        winner_stat: stat = {}

        # if winner is a tuple, then it is a tie
        if type(winner) == type(tuple()):
            # get average of both
            winner1, winner2 = winner
            winner_health = mean([winner1.health, winner2.health])

            # save winner's stats
            winner_stat = {
                'damage': mean([winner1.damage, winner2.damage]),
                'protection': mean([winner1.protection, winner2.protection]),
                'speed': mean([winner1.speed, winner2.speed]),
                'specie': winner1.__class__.__name__,
            }

        else:
            # save winner's stats
            winner_health = winner.health
            winner_stat = {
                'damage': winner.damage,
                'protection': winner.protection,
                'speed': winner.speed,
                'specie': winner.__class__.__name__,
            }

        # save fight data (including winner's stats)
        self.fights[game_data['game']][(game_data['iteration'], game_data['day'], game_data['fight_num'])] = {
            'winner_stat': winner_stat,
            'winner': winner,
            'loser': loser,
            'winner_remaining_health': winner_health,
            'turns': turns,
        }


    def get_fights(self, game: int, iteration: int = None):

        # depending on if iteration is given, return all fights or just the ones for that iteration (but always for one game process)
        if iteration is not None:
            return [v for k, v in self.fights[game].items() if k[1] == iteration]
        else:
            return [v for k, v in self.fights[game].items()]

    def save(self, entry: tuple[int, int] = False, average_data_location='./data/average_stats.csv', best_data_location='./data/best_stats.csv'):
        """
        saves a csv file with the best stats for each game and day and the average stats for each game and iteration
        if entry, then just add to bottom of file (not go through all data)
        """

        # make sure data folder exists
        if not os.path.exists('data'):
            os.makedirs('data')

        # the headings for the csv file
        headings = [
            'game',
            'iteration',
            'specie',
            'speed',
            'damage',
            'protection',
            'winner_remaining_health',
            'turns'
        ]

        # format the data to be written to the csv file
        def format_data(data: dict, game: int, iteration: int):
            return [
                game,
                iteration,
                data['stats']['specie'],
                data['stats']['speed'],
                data['stats']['damage'],
                data['stats']['protection'],
                data['winner_remaining_health'],
                data['turns']
            ]

        # if only one entry to write
        if entry:
            with open(average_data_location, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(format_data(self.average_data[entry], entry[0], entry[1]))

            with open(best_data_location, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(format_data(self.best_data[entry], entry[0], entry[1]))

            return
        
        # otherwise, go through all data and write to csv file
        with open(average_data_location, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for k, v in self.average_data.items():
                writer.writerow(format_data(v, k[0], k[1]))

        with open(best_data_location, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for k, v in self.best_data.items():
                writer.writerow(format_data(v, k[0], k[1]))
                

    average_data: dict[tuple[int, int], dict] = {}
    """
    ```
    (game, iteration): {
        'stats': {
            'damage': 15,
            'protection': 15,
            'speed': 15,
            'specie': 'human',
        },
        'winner_remaining_health': 0.1,
        'turns': 5,
    }
    ```
    """

    best_data: dict[tuple[int, int], dict] = {}
    """
    ```
    (game, iteration): {
        'stats': {
            'damage': 15,
            'protection': 15,
            'speed': 15,
            'specie': 'human',
        },
        'winner_remaining_health': 0.1,
        'turns': 5,
    }
    ```
    """

    def simplify_data(self, game: int, iteration: int):
        """
        puts data in average_data and best_data
        """

        # if interaction not specified, then print warning, and get all data
        if not iteration: print('iteration not specified')

        fights = self.get_fights(game, iteration).copy()

        # 
        if len(fights) == 0:
            print('no fights to simplify')
            return None

        # get average of all stats
        average_stats = {
            'damage': mean([fight['winner_stat']['damage'] for fight in fights]),
            'protection': mean([fight['winner_stat']['protection'] for fight in fights]),
            'speed': mean([fight['winner_stat']['speed'] for fight in fights]),
            'specie': fights[0]['winner_stat']['specie'],
        }

        # add to average_data
        self.average_data[(game, iteration)] = {
            'stats': average_stats,
            'winner_remaining_health': mean([fight['winner_remaining_health'] for fight in fights]),
            'turns': mean([fight['turns'] for fight in fights]),
        }

        # get best stats
        highest_remaining_health = 0
        for fight in fights:
            if fight == {}: continue

            if fight['winner_remaining_health'] > highest_remaining_health:
                highest_remaining_health = fight['winner_remaining_health']
                best = fight.copy()
                self.best_data[(game, iteration)] = {
                    'stats': best['winner_stat'],
                    'winner_remaining_health': best['winner_remaining_health'],
                    'turns': best['turns'],
                }


    def get_best_stat_overall(self) -> stat:
        """
        gets the best across all games and iterations
        """

        best = {
            'winner_remaining_health': 0,
        }

        # go through all data and find the best (by winner_remaining_health)
        for k, v in self.best_data.items():
            if v['winner_remaining_health'] > best['winner_remaining_health']:
                best = v.copy()

        return best['stats']
