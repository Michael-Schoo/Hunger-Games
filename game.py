import asyncio
from day import Day
from gui import GUI
from person.BasePerson import BasePerson as Person
from stats import Stats
from random_person import get_random_person
import concurrent.futures
import json


class Game():

    def __init__(self, game_id: int, iteration: int, stats: Stats, stat_closeness=10, players_amount=100):
        """
        The game class is responsible for spawning the days and one thread of the game
        """
        self.game_id = game_id
        self.iteration = iteration
        self.stats = stats

        self.stat_closeness = stat_closeness

        self.players = self.choose_players(players_amount)

    def choose_players(self, players_amount) -> list[Person]:
        """
        Chooses the players for the game
        """
        players = []
        best_player_stats = None

        # only try to get best stats if there is a previous iteration
        if self.iteration > 1:
            best_player_stats = self.stats.best_data[(
                self.game_id, self.iteration - 1)]['stats']

        # make all the players
        for i in range(players_amount):
            player = get_random_person(
                best_player_stats, self.stat_closeness, person_num=i+1)
            players.append(player)

        return players

    def get_alive_players(self) -> tuple[Person, Person]:
        """
        Gets the alive and dead players
        """
        alive_players = []
        dead_players = []
        for person in self.players:
            if person.get_health() > 0:
                alive_players.append(person)
            else:
                dead_players.append(person)

        return alive_players, dead_players

    def main(self):
        """
        Runs the game
        """
        day_num = 1
        alive_people, _ = self.get_alive_players()

        # run while there is more than one person alive
        while len(alive_people) > 1:
            day = Day(self.stats, self.players, game_data={'game': self.game_id, 'day': day_num, 'iteration': self.iteration})
            day.run()
            day_num += 1

            # make sure to update the alive people
            alive_people, _ = self.get_alive_players()


def game_runner(iterations: int, parallel_id: int, stats: Stats, players: int = 1000, save_unneeded_data=False, gui: GUI = None):
    # go through all the iterations (aka evolutions)
    for iteration in range(1, iterations+1):
        game = Game(parallel_id, iteration, stats, iterations - iteration, players)
        game.main()
        stats.simplify_data(parallel_id, iteration)

        # print that game's best stat
        if gui:
            gui.update()
        else:
            print(str(game.game_id), str(iteration), game.stats.best_data[(parallel_id, iteration)]['stats'], '\n')

        # remove the unneeded data (not needed for the next iteration)
        if not save_unneeded_data:
            stats.fights[parallel_id] = {}

        # save the data to csv
        stats.save(entry=(parallel_id, iteration))


async def async_game(*inputs):
    """
    function to run the game in a thread
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, game_runner, *inputs)


if __name__ == '__main__':
    players = int(input("Players: "))
    parallel_games = int(input("Parallel Games: "))
    iterations = int(input("Games to run (in each parallel): "))

    # Needed because if to many games at at time it can crash with the freeing up of resources
    # save_unneeded_data = input("Save unneeded data? (y/N): ").lower() == 'y'
    save_unneeded_data = False

    stats = Stats(parallel_games)
    gui = GUI(stats)

    # save metadata
    with open('data/metadata.json', 'w') as f:
        metadata = {
            'parallel_games': parallel_games,
            'iterations': iterations,
            'players': players,
            'in_progress': True,
        }
        json.dump(metadata, f)

    # reset the csv files
    stats.save()

    # run the games (either in parallel or not)
    if parallel_games == 1:
        game_runner(iterations, 0, stats, players, save_unneeded_data, gui)

    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # run the games in parallel
            async def run_async_matches():
                tasks = []
                for parallel_id in range(parallel_games):
                    tasks.append(asyncio.ensure_future(async_game(iterations, parallel_id, stats, players, save_unneeded_data, gui)))

                await asyncio.gather(*tasks)

            asyncio.run(run_async_matches())

    # save the best stats (and print them out)
    best_stat = stats.get_best_stat_overall()
    print(f"""\n\nBest stats below:
 - Damage: {best_stat['damage']}
 - Protection: {best_stat['protection']}
 - Speed: {best_stat['speed']}
 - Specie: {best_stat['specie']}
""")
    stats.save()

    # save metadata
    with open('data/metadata.json', 'w') as f:
        metadata = {
            'parallel_games': parallel_games,
            'iterations': iterations,
            'players': players,
            'best_stat': best_stat,
            'in_progress': False,
        }
        json.dump(metadata, f)
