"""Build the minimum skill requirement history from update notes.

This module parses skill requirement lists from the repository's markdown
update files, tracks the highest requirements encountered over time, and
produces a chronological skill-front history for the game.
"""
import re
import sys
import datetime
from typing import Generator, NamedTuple, Unpack

from rshisttools.skills import Skill
from rshisttools.dates import GAME_RELEASE_DAY
from rshisttools.paths import DAY_OF_RELEASE_FILE
from rshisttools.walk import UpdateInfo, WalkOptions, get_updates


class Requirement(NamedTuple):
    """A minimum skill requirement together with the reason for it."""
    level: int
    reason: str


class IconInfo(NamedTuple):
    """Information about where a skill icon appears in the skill menu."""
    row: int
    column: int
    icon: str


type MinimumStates = dict[Skill, Requirement]


DAY_OF_RELEASE_UPDATEINFO = UpdateInfo('Day of release', DAY_OF_RELEASE_FILE, GAME_RELEASE_DAY)
REQUIRED_SKILL_REQUIREMENT_PATTERN = re.compile(r'^- \[[ ,x]\] (\d+) (\w+)(?: - \*(.*)\*)?$')
OPTIONAL_SKILL_REQUIREMENT_PATTERN = re.compile(r'^- \[[ ,x]\] \(!Optional\) (\d+) (\w+)(?: - \*(.*)\*)?$')
INITIAL_LEVELS: MinimumStates = {
    Skill.ATTACK: Requirement(1, "All players starts with level 1 Attack."),
    Skill.STRENGTH: Requirement(1, "All players starts with level 1 Strength."),
    Skill.DEFENCE: Requirement(1, "All players starts with level 1 Defence."),
    Skill.RANGED: Requirement(1, "All players starts with level 1 Ranged."),
    Skill.PRAYER: Requirement(1, "All players starts with level 1 Prayer."),
    Skill.MAGIC: Requirement(1, "All players starts with level 1 Magic."),
    Skill.CONSTITUTION: Requirement(10, 'All players starts with level 10 Constitution.'),
    Skill.MINING: Requirement(1, "All players starts with level 1 Mining."),
    Skill.SMITHING: Requirement(1, "All players starts with level 1 Smithing."),
    Skill.COOKING: Requirement(1, "All players starts with level 1 Cooking."),
    Skill.FIREMAKING: Requirement(1, "All players starts with level 1 Firemaking."),
    Skill.WOODCUTTING: Requirement(1, "All players starts with level 1 Woodcutting."),
}


def skill_front_history(enddate: datetime.date, /, with_optional: bool = False) -> list[tuple[UpdateInfo, MinimumStates]]:
    """Return the minimum skill front at each update up to a given date.

    The history starts from the day-of-release state and then records the
    minimum requirements after every relevant update in chronological order.
    """
    current_front = INITIAL_LEVELS
    minimum_skill_front_history = [(DAY_OF_RELEASE_UPDATEINFO, current_front)]

    for update, requirements in sorted(get_all_skill_updates(with_optional, end=enddate), key=lambda pair: pair[0].date):
        current_front = update_minimum_states(current_front, requirements)
        minimum_skill_front_history.append((update, current_front))

    return minimum_skill_front_history


def total_level(front: MinimumStates) -> int:
    """Return the sum of all minimum skill levels in a skill front."""
    return sum(requirement.level for requirement in front.values())


def get_all_skill_updates(with_optional: bool = False, **options: Unpack[WalkOptions]) -> Generator[tuple[UpdateInfo, MinimumStates], None, None]:
    """Yield updates that contain at least one skill requirement."""
    for update in get_updates(with_root=True, with_completed=True, with_partially_completed=True, **options):
        if skill_requirements := fetch_skill_requirements(update, with_optional):
            yield (update, skill_requirements)


def fetch_skill_requirements(update: UpdateInfo, with_optional: bool = False) -> MinimumStates:
    """Parse the skill requirements recorded in an update file.

    Args:
        update: The update note to parse.
        with_optional: If True, include optional requirements as well.
    """
    pattern = OPTIONAL_SKILL_REQUIREMENT_PATTERN if with_optional else REQUIRED_SKILL_REQUIREMENT_PATTERN

    # Fetch all skill goals in the file
    requirements: dict[Skill, Requirement] = {}
    try:
        with open(update.path) as filewrapper:
            for __match in filter(None, map(pattern.match, filewrapper.readlines())):
                level = int(__match.group(1))
                skill = Skill(__match.group(2).title())
                reason = __match.group(3)
                if skill not in requirements or level > requirements[skill].level:
                    requirements[skill] = Requirement(level, reason)

    except ValueError as error:
        print(f"Value error in '{update}' - {error}")
        sys.exit(1)

    return requirements


def update_minimum_states(front: MinimumStates, requirements: dict[Skill, Requirement]) -> MinimumStates:
    """Update a skill front with the highest requirement seen for each skill."""
    front = front.copy()
    for skill, (level, reason) in requirements.items():
        if skill not in front or level > front[skill].level:
            front[skill] = Requirement(level, reason)
    return front


if __name__ == '__main__':
    *_, (update, front) = skill_front_history(datetime.date.today())
    print("Skill front in the end of 2001.")
    print("==============================")
    for skill, (level, reason) in front.items():
        if reason:
            print(f"- {skill}: {level} - *{reason}*")
        else:
            print(f"- {skill}: {level}")
    print(f"Total level: {total_level(front)}")
