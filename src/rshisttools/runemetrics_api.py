"""Retrieve and interpret RuneScape skill data from the official API.

This module fetches the current profile overview from RuneMetrics, converts the
returned skill values into the project's :class:`Skill` enum, and can also
reduce the result to a specific historical date using the repository's level
cap rules.
"""
import time
import requests
import datetime

from rshisttools.skills import Skill
from rshisttools.dates import max_level
from rshisttools.constants import PLAYERNAME


RUNEMETRICS_API_LINK = f"https://apps.runescape.com/runemetrics/profile/profile?user={PLAYERNAME}&activities=20"
SKILLS_API_ID_LOOKUP = {
    0: Skill.ATTACK,
    1: Skill.DEFENCE,
    2: Skill.STRENGTH,
    3: Skill.CONSTITUTION,
    4: Skill.RANGED,
    5: Skill.PRAYER,
    6: Skill.MAGIC,
    7: Skill.COOKING,
    8: Skill.WOODCUTTING,
    9: Skill.FLETCHING,
    10: Skill.FISHING,
    11: Skill.FIREMAKING,
    12: Skill.CRAFTING,
    13: Skill.SMITHING,
    14: Skill.MINING,
    15: Skill.HERBLORE,
    16: Skill.AGILITY,
    17: Skill.THIEVING,
    18: Skill.SLAYER,
    19: Skill.FARMING,
    20: Skill.RUNECRAFTING,
    21: Skill.HUNTER,
    22: Skill.CONSTRUCTION,
    23: Skill.SUMMONING,
    24: Skill.DUNGEONEERING,
    25: Skill.DIVINATION,
    26: Skill.INVENTION,
    27: Skill.ARCHAEOLOGY,
    28: Skill.NECROMANCY,
}


class LevelOverview:
    """Container for a player's skill levels and XP values."""
    xp: dict[Skill, int]
    levels: dict[Skill, int]

    def __init__(self, levels: dict[Skill, int], xp: dict[Skill, int]) -> None:
        """Store the provided level and XP mappings."""
        self.xp = xp
        self.levels = levels
        assert not (exclusive_disjunct := set(self.levels) ^ set(self.xp)), f"'xp' and 'level' does not have the same skills: {exclusive_disjunct}"

    def __len__(self) -> int:
        return len(self.levels)

    def get_total_level(self) -> int:
        """Return the sum of all current skill levels."""
        return sum(level for level in self.levels.values())

    def get_total_xp(self) -> int:
        """Return the sum of all current skill XP values."""
        return sum(xp for xp in self.xp.values())

    def get_combat_level(self) -> int:
        """Calculate the combat level using equation in described in 'https://runescape.wiki/w/Combat_level'"""
        # !!!Beware of the bug in the RuneMetrics API - Rounding error on combat level!!!
        attack = self.levels[Skill.ATTACK]
        strength = self.levels[Skill.STRENGTH]
        defence = self.levels[Skill.DEFENCE]
        ranged = self.levels[Skill.RANGED]
        prayer = self.levels[Skill.PRAYER]
        magic = self.levels[Skill.MAGIC]
        constitution = self.levels[Skill.CONSTITUTION]
        summoning = self.levels.get(Skill.SUMMONING, 0)
        necromancy = self.levels.get(Skill.NECROMANCY, 0)
        return (
            13 * max(attack + strength, 2 * ranged, 2 * magic, 2 * necromancy) // 10
            + defence
            + constitution
            + prayer // 2
            + summoning // 2
        ) // 4


def get_ingame_overview(date: datetime.date = datetime.date.today()) -> LevelOverview:
    """Get level overview reduced to fit the maximum levels of a given date"""
    return reduce_overview_to_date(get_official_overview(), date)


def get_official_overview() -> LevelOverview:
    """Fetch official level overview of my account using the RuneMetrics API."""
    time.sleep(0.5)  # Limit the rate of the API call
    with requests.get(RUNEMETRICS_API_LINK) as source:
        source_as_json = source.json()

    total_xp = int(source_as_json['totalxp'])
    total_level = int(source_as_json['totalskill'])
    combat_level = int(source_as_json["combatlevel"])

    xp = {}
    levels = {}
    for entry in source_as_json['skillvalues']:
        skill = SKILLS_API_ID_LOOKUP[entry['id']]
        xp[skill] = int(entry['xp']) // 10  # XP are stored with first decimal point: 123.4 -> 1234
        levels[skill] = int(entry['level'])

    overview = LevelOverview(levels, xp)
    assert overview.get_total_level() == total_level, f"Total level does not match API - {overview.get_total_level() - total_level}"
    assert overview.get_total_xp() == total_xp, f"Total XP does not match API - {overview.get_total_xp()} vs. {total_xp}"
    assert overview.get_combat_level() == combat_level, f"Combat level does not match API - {overview.get_combat_level()} vs. {combat_level}"

    return overview


def reduce_overview_to_date(overview: LevelOverview, date: datetime.date) -> LevelOverview:
    """Reduce the overview so it fits the given historical date.

    Unreleased skills are removed from the overview, and existing levels are
    capped to the maximum allowed for that date.
    """
    xp = {}
    levels = {}
    for skill in Skill:
        if (level := min(overview.levels[skill], max_level(skill, date))):
            levels[skill] = level
            xp[skill] = overview.xp[skill]
    return LevelOverview(levels, xp)


if __name__ == '__main__':
    from rshisttools.dates import current_ingame_date
    from rshisttools.skills import COMBAT_SKILLS
    official_overview = get_official_overview()
    reduced_overview = reduce_overview_to_date(official_overview, current_ingame_date())

    print("My official levels:")
    print(f"- Combat level is: {official_overview.get_combat_level()}")
    print(f"- Total level is: {(official_total := official_overview.get_total_level())}")
    print(f"- XP: {official_overview.get_total_xp()}")
    print()

    print("My unofficial levels:")
    print(f"- Combat level is: {reduced_overview.get_combat_level()}")
    print(f"- Total level is: {(unofficial_total := reduced_overview.get_total_level())}")
    print(f"- XP: {reduced_overview.get_total_xp()}")
    print()

    print(f"I have to subtract {official_total - unofficial_total} from my official total level to get my unofficial total level.")
    print()

    print("Combat skill levels:")
    for skill in COMBAT_SKILLS:
        print(f"- {skill}: {official_overview.levels[skill]}")
