"""
Module containing the different skills
"""
import enum


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


if __name__ == '__main__':
    print("Free-to-play skills:")
    for skill in FREE_TO_PLAY_SKILLS:
        print(f'- {skill}')
    print("Pay-to-play skills:")
    for skill in MEMBER_SKILLS:
        print(f'- {skill}')
    assert not (overlap := FREE_TO_PLAY_SKILLS & MEMBER_SKILLS), f"Overlap between member and free-to-play: {overlap}"
