from stats import Stats
from tabulate import tabulate


class GUI():
    def __init__(self, stats: Stats):
        self.stats = stats

    in_progress = False

    def update(self):
        # only run if not already running (to prevent weird console output)
        # if self.in_progress:  return

        # or wait until it is done
        while self.in_progress: pass
        self.in_progress = True

        # get the data
        average_data = self.stats.average_data.copy()  # the average for each game
        best_data = self.stats.average_data.copy()  # the best for each game

        # sort best_data (by thread_num, then game_num)
        best_data = sorted(best_data.items(), key=lambda x: (x[0][0], x[0][1]))
        table = []
        headers = ["Thread", "Game", "Specie", "Speed", "Damage", "Protection", "Remaining Health"]


        # Iterate over the best_data
        for (thread_num, game_num), best_stats in best_data:
            stats = best_stats.get('stats', {})

            # Add a row to the table
            row = [
                thread_num+1,
                game_num,
                stats.get('specie'),
                stats.get('speed'),
                stats.get('damage'),
                stats.get('protection'),
                best_stats.get('winner_remaining_health'),
            ]
            table.append(row)
        
        # Print the table
        tbl = tabulate(table, headers=headers, tablefmt="pipe", floatfmt=".2f")
        
        # Clear the console
        print("\033[H\033[J")
        print(tbl)

        self.in_progress = False
