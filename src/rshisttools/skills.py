"""
Module containing the different skills
"""
import enum
import json
from typing import NamedTuple
from rshisttools.paths import TABLE_FOLDER


class Skill(enum.StrEnum):
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
    MINING = 'Mining'
    SMITHING = 'Smithing'
    FISHING = 'Fishing'
    COOKING = 'Cooking'
    FIREMAKING = 'Firemaking'
    WOODCUTTING = 'Woodcutting'
    FARMING = 'Farming'
    SUMMONING = 'Summoning'
    INVENTION = 'Invention'


class IconInfo(NamedTuple):
    row: int
    column: int
    icon: str


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
FREE_TO_PLAY_SKILLS = set(Skill) - MEMBER_SKILLS


# Load the skill icons and their placement in the skill menu
with open(TABLE_FOLDER.joinpath('skill_icons.json')) as filewrapper:
    SKILL_ICONS = {
        Skill(info['skill']): IconInfo(row=info['row'], column=info['column'], icon=info['icon'])
        for info in json.load(filewrapper)
    }


if __name__ == '__main__':
    print("Free-to-play skills:")
    for skill in FREE_TO_PLAY_SKILLS:
        print(f'- {skill}')
    print("Pay-to-play skills:")
    for skill in MEMBER_SKILLS:
        print(f'- {skill}')
    assert not (overlap := FREE_TO_PLAY_SKILLS & MEMBER_SKILLS), f"Overlap between member and free-to-play: {overlap}"
