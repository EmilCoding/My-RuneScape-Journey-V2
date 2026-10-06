"""Path constants for the RuneScape history project.

This module centralizes the repository-relative paths used by the package.
It resolves the project root from the location of this file and exposes
constants for the main data folders, documentation files, and completed-year
folders.
"""
import pathlib


ROOT = pathlib.Path(__file__).parent.parent.parent
"""Path to the root of the project.

**Use this as a reference point for all other paths in the project.**
"""
assert ROOT.exists(), "Root path does not exists"
assert ROOT.joinpath('src').exists(), "Root path does not point to the root of the project"


# ============================================================================================================================ #
# Top-level content folders used throughout the project.                                                                       #
# ============================================================================================================================ #
FUTURE_GOALS = ROOT.joinpath('future goals')
"""Path to the folder containing all future update files."""
assert FUTURE_GOALS.exists(), "Future folder does not exists."


COMPLETED_GOALS = ROOT.joinpath('completed goals')
"""Path to the folder containing all completed update files."""
assert COMPLETED_GOALS.exists(), "Completed folder does not exists."


PARTIALLY_COMPLETED = ROOT.joinpath('partially completed')
"""Path to the folder containing all partially completed files."""
assert PARTIALLY_COMPLETED.exists(), "Partially completed folder does not exists."


TABLE_FOLDER = ROOT.joinpath('tables')
"""Path to the folder containing tables."""
assert TABLE_FOLDER.exists(), "Path to table file does not exists."


GRAPHICS_FOLDER = ROOT.joinpath('graphics')
"""Path to the folder containing graphical figures used in the project."""


# ============================================================================================================================ #
# Key repository files referenced by the package.                                                                              #
# ============================================================================================================================ #
README = ROOT.joinpath('README.md')
"""Path to the REAMDME.md file. The front face of the project."""
assert README.exists(), "README.md does not exists."


CURRENT_SKILL_FRONT = ROOT.joinpath('minimum-skill-front.md')
"""Path to the file containing the minumum-skill-front.

This file describes the current highest level skilling goal for each skill
as well as an overview of them. It functions as a minimum skill requirement
for the given date.
"""
assert CURRENT_SKILL_FRONT.exists(), "Current skill front does not exists!"


UPDATE_OVERVIEW = ROOT.joinpath('overview.json')
"""Path to the file containing a list of """


DAY_OF_RELEASE_FILE = COMPLETED_GOALS.joinpath('RuneScape Classic', '2001', '2001.01.04 - Day of release.md')
"""Path to the update file describing the day of release of RuneScape."""
assert DAY_OF_RELEASE_FILE, "Day-of-release file does not exists."


RAW_UPDATES_TABLE_FILE = TABLE_FOLDER.joinpath('raw-updates-fetched-from-wiki.json')
"""Update file containing the raw pull from the RuneScape wiki's update page.
This JSON file contains:
- The name of the update
- The link to the update page
- The date of the update.
"""
assert RAW_UPDATES_TABLE_FILE.exists(), """Path to the raw update file does not exists."""


TEMPLATE_FILE = ROOT.joinpath('update-template.md')
"""Path to the template used to generate update files."""
assert TEMPLATE_FILE.exists(), "Path to template file does not exists."


COMPLETED_FOLDERS = {
    # RuneScape Classic
    2001: COMPLETED_GOALS.joinpath('RuneScape Classic', '2001'),
    2002: COMPLETED_GOALS.joinpath('RuneScape Classic', '2002'),
    2003: COMPLETED_GOALS.joinpath('RuneScape Classic', '2003'),

    # RuneScape 2
    2004: COMPLETED_GOALS.joinpath('RuneScape 2', '2004'),
    2005: COMPLETED_GOALS.joinpath('RuneScape 2', '2005'),
    2006: COMPLETED_GOALS.joinpath('RuneScape 2', '2006'),
    2007: COMPLETED_GOALS.joinpath('RuneScape 2', '2007'),
    2008: COMPLETED_GOALS.joinpath('RuneScape 2', '2008'),
}
"""Dictonary that maps a year to its given update folder."""


if __name__ == '__main__':
    print(f'Root path is currently set to be "{ROOT}"')

    # Test if all the paths exist or not
    exceptions: list[KeyError | FileNotFoundError] = []
    for year, path in COMPLETED_FOLDERS.items():
        if not path.exists():
            exceptions.append(FileNotFoundError(f"{path=} does not exists"))
        if year != int(path.name):
            exceptions.append(KeyError(f"{year=} and {path.name} does not match"))

    if exceptions:
        raise ExceptionGroup("Some completed folders do not exist", exceptions)
    print("Path module is all okay.")
