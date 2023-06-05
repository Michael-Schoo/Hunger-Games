# plots data/stats.csv to matplotlib

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os


def plot_stats():
    # very similar to plot_stats, but it plots average stats and best stats on the same graph

    best_location = './data/best_stats.csv'
    average_location = './data/average_stats.csv'
    metadata_location = './data/metadata.json'

    if not os.path.exists(best_location):
        print(f'File {best_location} does not exist')
        return

    if not os.path.exists(average_location):
        print(f'File {average_location} does not exist')
        return

    if not os.path.exists(metadata_location):
        print(f'File {metadata_location} does not exist')
        return

    best_df = pd.read_csv(best_location)
    average_df = pd.read_csv(average_location)
    metadata = json.load(open(metadata_location))

    # plt.figure()
    # make the plot for the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # get the games
    games = best_df['game'].unique()

    # get the iterations
    iterations = best_df['iteration'].unique()
    num_iterations = len(iterations)

    # get the number of games
    num_games = len(games)

    # get the width of each bar and x locations of the bars
    width = 1 / (num_games + 1)
    x = np.arange(num_iterations)

    # get the x locations of the bars for each game
    x = [x + i * width for i in range(num_games)]

    # get the winner remaining health for each game and iteration
    best_y = []
    for game in games:
        best_y.append(best_df[best_df['game'] == game]
                      ['winner_remaining_health'])

    # plot the bars for best stats
    for i in range(num_games):
        ax.bar(x[i], best_y[i], width,
               label=f'game {i}', color='steelblue', alpha=0.7)

    # get the average remaining health for each game and iteration
    average_y = []
    for game in games:
        average_y.append(
            average_df[average_df['game'] == game]['winner_remaining_health'])

    # plot the bars for average stats
    for i in range(num_games):
        ax.bar(x[i], average_y[i], width,
               label=f'game {i}', color='darkorange', alpha=0.8)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Winner Remaining Health')
    ax.set_xlabel('Iteration')
    ax.set_title(
        f"Winner Remaining Health by {metadata['iterations']} Iterations in {metadata['parallel_games']} Parallel Games")
    ax.set_xticks(x[0])
    ax.set_xticklabels(iterations)

    # add a legend (blue = best, orange = average) - only need 2
    # ax.legend(['Best', 'Average'])
    # above but average is on orange (above is blue for both)
    legend_elements = [
        Patch(facecolor='lightsteelblue', edgecolor='cornflowerblue',
              label='Best'),
        Patch(facecolor='orange', edgecolor='darkorange',
              label='Average')
    ]

    ax.legend(handles=legend_elements,)

    # save the figure
    fig.savefig('./data/remaining_health.png')
    plt.show()


if __name__ == '__main__':
    plot_stats()
