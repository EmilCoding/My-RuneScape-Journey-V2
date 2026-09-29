"""
Module contains important dates in RuneScape history as well as
the release dates and maximum levels of the skills.
"""
import re
import datetime
from typing import Literal
from rshisttools.skills import Skill
from rshisttools.walk import CURRENT_INGAME_DATE


DATE_PATTERN = re.compile(r"^(\d{1,2})\s*(\w*)\s*(\d{4})$")
r"""Regular expression pattern that describes dates on the form dd \<month name\> YYYY."""


MONTH_LOOKUP_TABLE = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}
"""Dictionary that maps the english names for the months to their respective number."""


# ============================================================================================================================ #
# Important dates.                                                                                                             #
# ============================================================================================================================ #
GAME_RELEASE_DAY = datetime.date(2001, 1, 4)
"""Release day of the game: 4. January 2001."""


RUNESCAPE_2_RELEASE_DAY = datetime.date(2004, 3, 29)
"""Release day of RuneScape 2: 29. March 2004."""


RUNESCAPE_3_RELEASE_DAY = datetime.date(2013, 7, 22)
"""Release day of RuneScape 3: 22. July 2013."""


MEMBERSHIP_RELEASE_DAY = datetime.date(2002, 2, 27)
"""Release day of membership: 27. February 2002."""


MODERN_OSRS_SPLIT_DATE = datetime.date(2007, 8, 10)
"""Date of the back-up that became Old School RuneScape: 10. August 2007."""


SIXTH_AGE_STARTS = datetime.date(2013, 3, 4)
"""Date where RuneScape moved from the fifth age to the sixth age: 4. March 2013.

(**!Spoilers!**) At the end of the World Wakes, Guthix is killed by Slikse.
The results the protective ward over Giellinor, the exiles the Gods, is removed.
This kick-starts the sixth age.
"""


SQUEAL_OF_FORTUNE_RELEASE_DAY = datetime.date(2012, 2, 28)
"""Release of the Squeal of fortune: 28. February 2012.

Gambling is now a feature of RuneScape where you can pay real life
money for spins. The rewards include experience lamps, money, powerful
items, skilling equipment, and much more. A clear low point in the game's
history.

Squeal of fortune was later reworked to treasure hunter, which didn't change
the fundamental mechanics.
"""


TREASURE_HUNTER_REMOVED = datetime.date(2026, 1, 19)
"""Removal of treasure hunter: 19. January 2026."""


FREE_TRADE_REMOVAL = datetime.date(2007, 12, 10)
"""Removal date of free trade: 10. December 2007.

Due to a big problem with real world trading web-sites, RuneScape was
appraced to the credit card companies due to large amount of fraud
involving said websites. To combat this, Jagex had to reach fast and
implement a trading limit.

This hit the player-base hard, and many quit the game. The game has never really
recovered from this.
"""


FREE_TRADE_RETURNS = datetime.date(2008, 1, 2)
"""Date where free trade was returned: 2. January 2008.

Although free-trade was reimplemented, the damage was already done.
"""


EVOLUTION_OF_COMBAT = datetime.date(2012, 11, 20)
"""Release date of the Evolution of Combat: 20 November 2012.

On this date, the most controvertial update was launched that changed
the combat system fundamentally. It resulted in many people quitting
which eventually resulted in the release of Old School RuneScape.
"""


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
"""
Skills release days
-------------------
- Tailoring was removed on 10 May 2001 and eventually replaced by crafting
- Influence was replaced by the Quest Point system on 10 May 2001
- Release of GoodMagic and EvilMagic is merged into Magic
- Release of PrayGood and PrayEvil is merged into Prayer
- Carpentry was removed on 12 December 2002 and eventually replaced by construction
"""


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
"""
Dates on which the maximum level of a skill was 110.
----------------------------------------------------
- On 12. August 2024, Mining and Smithing had their maximum levels increased to 110, the first skills to have a maximum level higher than 99 but less than 120.
- On 9. December 2024, Woodcutting, Fletching and Firemaking had their maximum levels increased to 110.
- On 3. March 2025, Runecrafting had its maximum level increased to 110.
- On 16. June 2025, Crafting had its maximum level increased to 110.
- On 23. March 2026, Hunter has its maximum level increased to 110.
"""


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
"""
Dates on which the maximum level of a skill was 120.
----------------------------------------------------
- The Dungeoneering skill was added on 12 April 2010, which has a maximum level of 120, rather than the maximum of 99 for previous skills.
- Invention was released on 25 January 2016 as the second 120 skill.
- On 5 June 2017, the Slayer skill had its maximum level raised from 99 to 120.
- On 25 November 2019, the Farming and Herblore skills had their maximum levels raised from 99 to 120.
- On 30 March 2020, Archaeology was released, which has a maximum level of 120.
- On 7 August 2023, Necromancy was released, which is the first combat skill to have a maximum level of 120.
- On 24 November 2025, the Thieving skill had its maximum level raised from 99 to 120.
- On 2 March 2026, Attack, Strength, Ranged, and Magic had their maximum levels raised from 99 to 120.
- On 13 July 2026, Construction had its maximum level raised from 99 to 120.
"""


def max_total_level(date: datetime.date = CURRENT_INGAME_DATE) -> int:
    """Calculate the maximum possible total level at a given date.

    Args:
        date (datetime.date, optional): Date for which the max. level is calculated for. Default is current ingame date.

    Returns:
        int: Max total level for the given date.
    """
    return sum(max_level(skill, date) for skill in Skill)


def max_level(skill: Skill, date: datetime.date = CURRENT_INGAME_DATE) -> Literal[120, 110, 99, 0]:
    """Return the maximum level of a given skill using a given date as reference.

    Args:
        skill (Skill): Skill in question.
        date (datetime.date, optional) Date for which the calculations are based on. Default is current ingame date.

    Returns:
        Literal[120, 110, 99, 0]: Maximum level of the given skill. 0 represents not being released yet.
    """
    if date < SKILL_RELEASE_DAYS[skill]:
        return 0
    if (x := LEVEL_120_SKILL_DATES.get(skill, None)) and date >= x:
        return 120
    if (x := LEVEL_110_SKILL_DATES.get(skill, None)) and date >= x:
        return 110
    return 99


def date_from_string(string: str) -> datetime.date:
    r"""Convert a string on the form: DD. \<Month name\> YYYY into a datetime.date instance."""
    if (match := DATE_PATTERN.match(string)) is None:
        raise ValueError(f'Cannot interpret {string} as date')
    day_str, month_str, year_str = match.groups()
    return datetime.date(year=int(year_str), month=MONTH_LOOKUP_TABLE[month_str], day=int(day_str))


MAX_TOTAL_LEVEL = max_total_level(datetime.date.today())
"""Maximum possible total level calculated from the current date. (Real life date.)"""


CURRENT_INGAME_MAX_TOTAL = max_total_level(CURRENT_INGAME_DATE)
"""Maximum possible total level calculated from the current in-game date."""


if __name__ == '__main__':
    MAX_TOTAL_LEVEL_FROM_WIKI = 3232  # Read from wikipedia https://runescape.wiki/w/Total_level - Last updated: 29. September 2026

    today = datetime.date.today()
    print(f"Max level at {today:%d %B %Y} is: {MAX_TOTAL_LEVEL}")
    assert MAX_TOTAL_LEVEL == MAX_TOTAL_LEVEL_FROM_WIKI, f"Total level calculations are wrong! - Missing {MAX_TOTAL_LEVEL_FROM_WIKI - MAX_TOTAL_LEVEL} levels"
