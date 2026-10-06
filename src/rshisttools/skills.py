"""
Module containing the skills of RuneScape as well as a dictionary of the
skill icons.
"""
import enum
import json
from typing import NamedTuple
from rshisttools.paths import TABLE_FOLDER


class Skill(enum.StrEnum):
    """Skills in the game of RuneScape 3."""
    # Column 1
    ATTACK = 'Attack'
    STRENGTH = 'Strength'
    DEFENCE = 'Defence'
    RANGED = 'Ranged'
    PRAYER = 'Prayer'
    MAGIC = 'Magic'
    RUNECRAFTING = 'Runecrafting'
    CONSTRUCTION = 'Construction'
    DUNGEONEERING = 'Dungeoneering'
    ARCHAEOLOGY = 'Archaeology'

    # Column 2
    CONSTITUTION = 'Constitution'
    AGILITY = 'Agility'
    HERBLORE = 'Herblore'
    THIEVING = 'Thieving'
    CRAFTING = 'Crafting'
    FLETCHING = 'Fletching'
    SLAYER = 'Slayer'
    HUNTER = 'Hunter'
    DIVINATION = 'Divination'
    NECROMANCY = 'Necromancy'

    # Column 3
    MINING = 'Mining'
    SMITHING = 'Smithing'
    FISHING = 'Fishing'
    COOKING = 'Cooking'
    FIREMAKING = 'Firemaking'
    WOODCUTTING = 'Woodcutting'
    FARMING = 'Farming'
    SUMMONING = 'Summoning'
    INVENTION = 'Invention'


MEMBER_SKILLS = {
    Skill.CONSTRUCTION,
    Skill.ARCHAEOLOGY,
    Skill.AGILITY,
    Skill.HERBLORE,
    Skill.THIEVING,
    Skill.SLAYER,
    Skill.HUNTER,
    Skill.DIVINATION,
    Skill.NECROMANCY,
    Skill.FARMING,
    Skill.SUMMONING,
    Skill.INVENTION,
}
"""Set containing all the members skills."""


FREE_TO_PLAY_SKILLS = set(Skill) - MEMBER_SKILLS
"""Set containing all the free-to-play skills. That is all non-member skills."""


COMBAT_SKILLS = {
    Skill.ATTACK,
    Skill.STRENGTH,
    Skill.DEFENCE,
    Skill.RANGED,
    Skill.PRAYER,
    Skill.MAGIC,
    Skill.CONSTITUTION,
    Skill.SUMMONING,
    Skill.NECROMANCY,
}
"""Set containing all the combat skills. That is skills that contributes to your combat level."""


class IconInfo(NamedTuple):
    """An (int, int, str) triplet containing:
    0. ´row´ is a positive integer describes the row number of the icon in the skill-menu.
    1. ´col´ is either 1, 2, and 3 and describes the column number of the icon in the skill-menu.
    2. ´icon´ is a string that can be placed in any markdown file and renderes as a skill icon.
      The string pulls an icon from the RuneScape wiki.

    Row and column index both 1 indexed.
    """
    row: int
    """1-indexed row index of given skill icon in skill menu."""

    column: int
    """1-indexed column index of given skill icon in skill menu."""

    icon: str
    """String that can be placed in any markdown file and renderes as a skill icon."""


@lambda _: _()
def SKILL_ICONS() -> dict[str, IconInfo]:
    """Dictionary that maps Skills to a triplet containing skill-icon and its placement in the skill menu."""
    with open(TABLE_FOLDER.joinpath('skill_icons.json')) as filewrapper:
        return {
            info['skill']: IconInfo(row=info['row'], column=info['column'], icon=info['icon'])
            for info in json.load(filewrapper)
        }


if __name__ == '__main__':
    print("Free-to-play skills:")
    for skill in FREE_TO_PLAY_SKILLS:
        print(f'- {skill}')
    print("Pay-to-play skills:")
    for skill in MEMBER_SKILLS:
        print(f'- {skill}')
