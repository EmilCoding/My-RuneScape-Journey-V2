"""
Module contains important dates in RuneScape history as well as
the release dates and maximum levels of the skills.

Last updates: 3 August 2026.
"""
import re
import calendar
import datetime
from typing import Literal
from rshisttools.skills import Skill
from rshisttools.walk import current_ingame_date


CURRENT_INGAME_DATE = current_ingame_date()
DATE_PATTERN = re.compile(r"^(\d{1,2})\s*(\w*)\s*(\d{4})$")
MONTH_LOOKUP_TABLE = {name: i for i, name in enumerate(calendar.month_name) if name}


# Important dates
GAME_RELEASE_DAY = datetime.date(2001, 1, 4)
RUNESCAPE_2_RELEASE_DAY = datetime.date(2004, 3, 29)
RUNESCAPE_3_RELEASE_DAY = datetime.date(2013, 7, 22)
MEMBERSHIP_RELEASE_DAY = datetime.date(2002, 2, 27)
MODERN_OSRS_SPLIT_DATE = datetime.date(2007, 8, 10)
SIXTH_AGE_STARTS = datetime.date(2013, 3, 4)
SQUEAL_OF_FORTUNE_RELEASE_DAY = datetime.date(2012, 2, 28)
TREASURE_HUNTER_REMOVED = datetime.date(2026, 1, 19)
FREE_TRADE_REMOVAL = datetime.date(2007, 12, 10)
FREE_TRADE_RETURNS = datetime.datetime(2008, 1, 2)


# Skills release days
# -------------------
# Tailoring was removed on 10 May 2001 and eventually replaced by crafting
# Influence was replaced by the Quest Point system on 10 May 2001
# Release of GoodMagic and EvilMagic is merged into Magic
# Release of PrayGood and PrayEvil is merged into Prayer
# Carpentry was removed on 12 December 2002 and eventually replaced by construction
SKILL_RELEASE_DAYS = {
    Skill.ATTACK: GAME_RELEASE_DAY,
    Skill.STRENGTH: GAME_RELEASE_DAY,
    Skill.DEFENCE: GAME_RELEASE_DAY,
    Skill.RANGED: GAME_RELEASE_DAY,
    Skill.PRAYER: GAME_RELEASE_DAY,
    Skill.MAGIC: GAME_RELEASE_DAY,
    Skill.MINING: GAME_RELEASE_DAY,
    Skill.SMITHING: GAME_RELEASE_DAY,
    Skill.CONSTITUTION: GAME_RELEASE_DAY,
    Skill.COOKING: GAME_RELEASE_DAY,
    Skill.FIREMAKING: GAME_RELEASE_DAY,
    Skill.WOODCUTTING: GAME_RELEASE_DAY,
    Skill.CRAFTING: datetime.date(2001, 5, 8),
    Skill.FISHING: datetime.date(2001, 6, 11),
    Skill.HERBLORE: datetime.date(2002, 2, 27),
    Skill.FLETCHING: datetime.date(2002, 3, 25),
    Skill.THIEVING: datetime.date(2002, 4, 30),
    Skill.AGILITY: datetime.date(2002, 12, 12),
    Skill.RUNECRAFTING: datetime.date(2004, 3, 29),
    Skill.SLAYER: datetime.date(2005, 1, 26),
    Skill.FARMING: datetime.date(2005, 7, 11),
    Skill.CONSTRUCTION: datetime.date(2006, 5, 31),
    Skill.HUNTER: datetime.date(2006, 11, 21),
    Skill.SUMMONING: datetime.date(2008, 1, 15),
    Skill.DUNGEONEERING: datetime.date(2010, 4, 12),
    Skill.DIVINATION: datetime.date(2013, 8, 20),
    Skill.INVENTION: datetime.date(2016, 1, 25),
    Skill.ARCHAEOLOGY: datetime.date(2020, 3, 30),
    Skill.NECROMANCY: datetime.date(2023, 8, 7),
}


# Dates on which the maximum level of a skill was 110.
# ----------------------------------------------------
# On 12 August 2024, Mining and Smithing had their maximum levels increased to 110, the first skills to have a maximum level higher than 99 but less than 120.
# On 9 December 2024, Woodcutting, Fletching and Firemaking had their maximum levels increased to 110.
# On 3 March 2025, Runecrafting had its maximum level increased to 110.
# On 16 June 2025, Crafting had its maximum level increased to 110.
LEVEL_110_SKILL_DATES = {
    Skill.MINING: datetime.date(2024, 8, 12),
    Skill.SMITHING: datetime.date(2024, 8, 12),
    Skill.WOODCUTTING: datetime.date(2024, 12, 9),
    Skill.FLETCHING: datetime.date(2024, 12, 9),
    Skill.FIREMAKING: datetime.date(2024, 12, 9),
    Skill.RUNECRAFTING: datetime.date(2025, 3, 3),
    Skill.CRAFTING: datetime.date(2025, 6, 16),
    Skill.HUNTER: datetime.date(2026, 3, 23),
}

# Dates on which the maximum level of a skill was 120.
# ----------------------------------------------------
# The Dungeoneering skill was added on 12 April 2010, which has a maximum level of 120, rather than the maximum of 99 for previous skills.
# Invention was released on 25 January 2016 as the second 120 skill.
# On 5 June 2017, the Slayer skill had its maximum level raised from 99 to 120.
# On 25 November 2019, the Farming and Herblore skills had their maximum levels raised from 99 to 120.
# On 30 March 2020, Archaeology was released, which has a maximum level of 120.
# On 7 August 2023, Necromancy was released, which is the first combat skill to have a maximum level of 120.
# On 24 November 2025, the Thieving skill had its maximum level raised from 99 to 120.
# On 2 March 2026, Attack, Strength, Ranged, and Magic had their maximum levels raised from 99 to 120.
# On 13 July 2026, Construction had its maximum level raised from 99 to 120.
LEVEL_120_SKILL_DATES = {
    Skill.DUNGEONEERING: SKILL_RELEASE_DAYS[Skill.DUNGEONEERING],
    Skill.INVENTION: SKILL_RELEASE_DAYS[Skill.INVENTION],
    Skill.SLAYER: datetime.date(2017, 6, 5),
    Skill.FARMING: datetime.date(2019, 11, 25),
    Skill.HERBLORE: datetime.date(2019, 11, 25),
    Skill.ARCHAEOLOGY: SKILL_RELEASE_DAYS[Skill.ARCHAEOLOGY],
    Skill.NECROMANCY: SKILL_RELEASE_DAYS[Skill.NECROMANCY],
    Skill.THIEVING: datetime.date(2025, 11, 24),
    Skill.ATTACK: datetime.date(2026, 3, 2),
    Skill.STRENGTH: datetime.date(2026, 3, 2),
    Skill.RANGED: datetime.date(2026, 3, 2),
    Skill.MAGIC: datetime.date(2026, 3, 2),
    Skill.ATTACK: datetime.date(2026, 3, 2),
    Skill.STRENGTH: datetime.date(2026, 3, 2),
    Skill.RANGED: datetime.date(2026, 3, 2),
    Skill.MAGIC: datetime.date(2026, 3, 2),
    Skill.CONSTRUCTION: datetime.date(2026, 7, 13),
}


def max_total_level(date: datetime.date) -> int:
    """Calculate the maximum total level at a given date"""
    return sum(max_level(skill, date) for skill in Skill)


def max_level(skill: Skill, date: datetime.date) -> Literal[120, 110, 99, 0]:
    """Return the maximum level of a given skill given a date."""
    if date < SKILL_RELEASE_DAYS[skill]:
        return 0
    if (__date := LEVEL_120_SKILL_DATES.get(skill, None)) and date >= __date:
        return 120
    if (__date := LEVEL_110_SKILL_DATES.get(skill, None)) and date >= __date:
        return 110
    return 99


def date_from_string(string: str) -> datetime.date:
    if not (__match := DATE_PATTERN.match(string)):
        raise ValueError(f'Cannot interpret {string} as date')
    return datetime.date(
        int(__match.group(3)),
        MONTH_LOOKUP_TABLE[__match.group(2)],
        int(__match.group(1))
    )


if __name__ == '__main__':
    MAX_TOTAL_LEVEL = 3232  # Picked from wikipedia https://runescape.wiki/w/Total_level

    today = datetime.date.today()
    total_level = max_total_level(today)
    print(f"Max level at {today:%d %B %Y} is: {total_level}")
    assert MAX_TOTAL_LEVEL == total_level, "Total level calculations are wrong! - Missing {MAX_TOTAL_LEVEL - total_level} levels"
