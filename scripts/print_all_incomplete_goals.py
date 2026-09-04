"""
Walk throught all completed or partially completed updates
and count the number of incomplete goals.

Also check if any incomplete goals are in the `completed` folder
"""
import colorama
import warnings
from rshisttools.paths import COMPLETED_GOALS, PARTIALLY_COMPLETED
from rshisttools.walk import INCOMPLETE_GOALS_PATTERN, get_updates


n_incomplete_goals = 0
n_incomplete_updates = 0
for update in sorted(get_updates(with_partially_completed=True, with_completed=True)):
    incomplete_goals = []
    with open(update.path, 'r') as filewrapper:
        for line in filewrapper.readlines():
            if INCOMPLETE_GOALS_PATTERN.match(line):
                incomplete_goals.append(line)
                n_incomplete_goals += 1

    # If file has incomplet goals, print them to consol
    if incomplete_goals:
        n_incomplete_updates += 1
        print("".join([f"{update}\n", *incomplete_goals]))

    # Check if file is placed in the correct folder
    if incomplete_goals and update.path.is_relative_to(COMPLETED_GOALS):
        warnings.warn(colorama.Fore.YELLOW + f'Incomplete goals in completed folder: {update.path}' + colorama.Fore.RESET)
    if not incomplete_goals and update.path.is_relative_to(PARTIALLY_COMPLETED):
        warnings.warn(colorama.Fore.YELLOW + f'No incomplete goals in partially completed folder: {update.path}' + colorama.Fore.RESET)

print(f"Number of incomplete goals: {n_incomplete_goals}")
print(f"Number of incomplete updates: {n_incomplete_updates}")
