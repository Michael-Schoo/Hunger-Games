import random
from day import Day
from person.BasePerson import BasePerson as Person
from person.person import people as people_options
from stats import Stats, stat


# the constants 
# the default range
STAT_RANGE_DELTA = 6

# the total stat sum
TOTAL_STAT_VALUE = 50

# the minimum stat value
MIN_STAT_VALUE = 5

# the maximum stat value
MAX_STAT_VALUE = TOTAL_STAT_VALUE - MIN_STAT_VALUE * 3


def get_stat_range(best_stat: int | None, allowed_difference: int):
    """
    Gets the range of a stat
    """
    # uses the best stat if it exists
    if best_stat is not None:
        best_stat = round(best_stat)
        min_range = max(best_stat - allowed_difference, MIN_STAT_VALUE)
        max_range = min(best_stat + allowed_difference, MAX_STAT_VALUE)
    else:
        # otherwise, use the default range
        min_range, max_range = MIN_STAT_VALUE, MAX_STAT_VALUE

    return min_range, max_range

# the stat options to choose from
stat_options = ['speed', 'damage', 'protection']

def make_random_stats(best_stat: stat = None, allowed_difference = 6):
    remaining_total = TOTAL_STAT_VALUE

    stats = {}

    # set all stats to 0 by default
    for stat_name in stat_options: stats[stat_name] = 0

    # shuffle the stat options
    shuffled_stat_options = stat_options.copy()
    random.shuffle(shuffled_stat_options)

    # go through all the stats and set them to a random value (between the range)
    for stat_name in shuffled_stat_options:

        min_range, max_range = get_stat_range(best_stat[stat_name] if best_stat else None, allowed_difference)
        if min_range > max_range:
            stat = max_range
        else:
            stat = random.randint(min_range, max_range)
        stats[stat_name] = stat*50
        remaining_total -= stat*50

    if remaining_total > 0:
        # Adjust one of the stats to reach the target total
        stat_name = random.choice(stat_options)
        stats[stat_name] += remaining_total

    elif remaining_total < 0:
        # Adjust existing stats to compensate for negative remaining total
        stat_names = stat_options.copy()
        random.shuffle(stat_names)

        # because it is negative, we want to add to the stats to make it positive
        for stat_name in stat_names:
            remaining_adjustment = abs(remaining_total)
            if remaining_adjustment <= stats[stat_name] - MIN_STAT_VALUE:
                stats[stat_name] -= remaining_adjustment
                break
            else:
                remaining_adjustment = stats[stat_name] - MIN_STAT_VALUE
                stats[stat_name] = MIN_STAT_VALUE
            remaining_total += remaining_adjustment
    
    # finally, return the stats to be used
    return stats


def choose_specie(prev_specie) -> Person:
    # 75% of same
    random_num = random.randint(0, 100)
    if random_num < 75 and prev_specie is not None:
        for person in people_options:
            if person.__class__.__name__ == prev_specie:
                return person
            
    return random.choice(people_options)


def get_random_person(prev_winner: stat | None, allowed_difference: int | None, person_num = 1) -> Person:
    stats = make_random_stats(prev_winner, allowed_difference)
    person = choose_specie(prev_winner and prev_winner.get("speed"))(**stats)
    person.name = f'AI_{person.__class__.__name__}_{person_num}'

    return person

if __name__ == '__main__':
    # test for it to follow the rules - 50 total for all, 5 min each
    best_stat = {
        'speed': 10,
        'damage': 38,
        'protection': 2,
        # 'speed': 20,
        # 'damage': 15,
        # 'protection': 15,
    }

    print('testing... (1_000_000 iterations)')
    for i in range(1_000_000*100):
        stat = make_random_stats(best_stat)
        assert sum(stat.values()) == 50
        assert all([value >= 5 for value in stat.values()])
        
    print('test done!')


