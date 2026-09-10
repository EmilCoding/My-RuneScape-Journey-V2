"""
Library to handle and check all partially completed goals
"""
import re
import enum
import itertools
from typing import *

from rshisttools.walk import *

class Tags(enum.StrEnum):
    DROP = '#Drop'
    LEGENDARY = '#Legendary'
    OPTIONAL = enum.auto()


GOAL_WITH_TAGS = re.compile(r".*\((\#.*)\)")


def fetch_missing_goals(update: UpdateInfo) -> Generator[str, None, None]:
    with open(update.path, 'r') as filewrapper:
        for line in filewrapper.readlines():
            if __match := INCOMPLETE_GOALS_PATTERN.match(line):
                yield __match.group(1)


def collect_all_tags(goals: Iterable[str]):
    goals_and_tags = []
    for goal in goals:
        tags = []
        if '(!Optional)' in goal:
            tags.append(Tags.OPTIONAL)
        if '#' not in goal:
            goals_and_tags.append((goal, *tags))
            break

        # if __match := GOAL_WITH_TAGS.match(goal):
        #     print(__match)

            # group(1).split(','):

        

        # goals_and_tags.append((goal, *tags))

    return goals_and_tags



# Print all non-completed goals to consol with appropriate tags
if __name__ == '__main__':
    updates = get_updates(with_partially_completed=True)
    count = 0
    goals = itertools.chain(*map(fetch_missing_goals, updates))

    for element in collect_all_tags(goals):
        print(f"- {element}")
        count += 1
    print(f"Number of goals: {count}")
