"""Path constants for the RuneScape history project.

This module centralizes the repository-relative paths used by the package.
It resolves the project root from the location of this file and exposes
constants for the main data folders, documentation files, and completed-year
folders.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent

# Top-level content folders used throughout the project.
FUTURE_GOALS = ROOT.joinpath('future goals')
COMPLETED_GOALS = ROOT.joinpath('completed goals')
PARTIALLY_COMPLETED = ROOT.joinpath('partially completed')
TABLE_FOLDER = ROOT.joinpath('tables')
GRAPHICS_FOLDER = ROOT.joinpath('graphics')

# Key repository files referenced by the package.
README = ROOT.joinpath('README.md')
CURRENT_SKILL_FRONT = ROOT.joinpath('minimum-skill-front.md')
UPDATE_OVERVIEW = ROOT.joinpath('overview.json')
DAY_OF_RELEASE_FILE = COMPLETED_GOALS.joinpath('RuneScape Classic', '2001', '2001.01.04 - Day of release.md')
RAW_UPDATES_FILE = TABLE_FOLDER.joinpath('raw-updates-fetched-from-wiki.json')

# Completed content folders grouped by year for quick access.
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


if __name__ == '__main__':
    print(f'Root path is currently set to be "{ROOT}"')
    assert ROOT.joinpath('src').exists(), "Root path does not exists"
    assert all(folder.is_dir() for folder in COMPLETED_FOLDERS.values()), "Some completed folders do not exist."
    print("Path module is all okay.")
