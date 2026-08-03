import re
import math
import click
import datetime
import urllib.parse

from rshisttools.paths import ROOT, README, CURRENT_SKILL_FRONT, FUTURE_GOALS, COMPLETED_FOLDERS, COMPLETED_GOALS
from rshisttools.skills import Skill, SKILL_ICONS
from rshisttools.runemetrics_api import LevelOverview, get_ingame_overview
from rshisttools.dates import CURRENT_INGAME_DATE, RUNESCAPE_2_RELEASE_DAY, max_total_level
from rshisttools.walk import UpdateInfo, DateRange, get_current_update_window, walk_updates

from rshisttools.skillfront import MinimumStates, skill_front_history

# Regex patterns
CURRENT_DATE_PATTERN = re.compile(r'- \[Current date\]\(.*\): .*')
TOTAL_LEVEL_PATTERN = re.compile(r'- Total level\:.*')
COMBAT_LEVEL_PATTERN = re.compile(r'- Combat level\:.*')
STATES_MENU_START_PATTERN = re.compile('<!-- Current skills start -->')
STATES_MENU_END_PATTERN = re.compile('<!-- Current skills end -->')
LAST_UPDATES_LINE_PATTERN = re.compile(r'\*Last updates: (.*)\*')


@click.group
def main() -> None:
    """Keeps the reposity up-to-date with my account and goals."""


@main.command
@click.pass_context
def update_public(ctx) -> None:
    """Update all files so they are ready for the public to read.

    This should be called before/on pushing to GitHub, so that the
    online public reposity is up-to-date.

    To-Do list:
    - Update README.md
    - Update current minimum-skill-front
    - Update end of year minimum-skill-fronts
    """
    ctx.invoke(update_readme)
    ctx.invoke(update_current_skill_front)


@main.command
def update_readme() -> None:
    """Update the README.md file so it reflects current state of the account.

    1) Update current update line
    2) Update current total level
    3) Update current combat level
    4) Update stats section
    """
    ingame_date = CURRENT_INGAME_DATE
    level_overview = get_ingame_overview(ingame_date)
    current_update, window = get_current_update_window()

    click.echo("Read content of ~/README.md file")
    with open(README, 'r') as filewrapper:
        lines = filewrapper.readlines()

    click.echo("Update lines of ~/README.md file")
    _update_current_update_line_in_readme(lines, current_update, window)
    _update_current_total_level_in_readme(lines, level_overview)
    _update_combat_level_in_readme(lines, level_overview)
    lines = _insert_states_in_readme(lines, level_overview)
    _set_last_updates_line(lines)

    click.echo("Save changes to ~/README.md")
    with open(README, 'w') as filewrapper:
        filewrapper.writelines(lines)


@main.command()
@click.pass_context
def update_skill_fronts(ctx) -> None:
    ctx.invoke(update_current_skill_front)
    ctx.invoke(end_of_year_skill_front)
    ctx.invoke(end_of_version_skill_front)


@main.command
def update_current_skill_front() -> None:
    """Update the current skill front in the 'minimum-skill-front.md' file in repository root."""
    *_, (update, skillfront) = skill_front_history(CURRENT_INGAME_DATE)

    click.echo("Update ~/minimum-skill-front.md")
    with open(CURRENT_SKILL_FRONT, 'w') as filewrapper:
        filewrapper.writelines(minimum_skill_front_markdown(update, skillfront))


@main.command
def end_of_year_skill_front() -> None:
    """Make end-of-year skill-front for every completed year in the repository.

    Each front is described in a markdown file with with a name generated from
    the 'filename_template' argument and and is saved in its respective completed year folder.
    """
    click.echo("Determine skill front history and extract them into years ")
    end_of_year_fronts: dict[int, tuple[UpdateInfo, MinimumStates]] = {}
    for update, skillfront in skill_front_history(CURRENT_INGAME_DATE):
        end_of_year_fronts[update.date.year] = (update, skillfront)

    # Remove current year if not done yet
    current_year = max(end_of_year_fronts)
    if current_year == min(walk_updates(FUTURE_GOALS), key=UpdateInfo.get_date).date.year:
        click.echo(f"Year {current_year} is finished - The minimum-skill-front cannot be made")
        end_of_year_fronts.pop(current_year)

    click.echo("Update minimum skill front for all completed years:")
    click.echo("--------------------------------------------------")
    for year, (update, skillfront) in end_of_year_fronts.items():
        click.echo(f"- Update end-of-year skill front of year {year}.")
        with open(COMPLETED_FOLDERS[year].joinpath('minimum-skill-front.md'), 'w') as filewrapper:
            filewrapper.writelines(minimum_skill_front_markdown_end_of_year(update, skillfront))


@main.command
def end_of_version_skill_front() -> None:
    """Write and end-of-version skill fronts for RuneScape classic, and later RuneScape 2"""
    history = skill_front_history(CURRENT_INGAME_DATE)

    # Find last update in RuneScape Classic
    *_, (_, skillfront) = filter(lambda pair: pair[0].date < RUNESCAPE_2_RELEASE_DAY, history)

    click.echo("Update minimum skill front for RuneScape Classic")
    with open(COMPLETED_GOALS.joinpath('RuneScape Classic', 'minimum-skill-front.md'), 'w') as filewrapper:
        filewrapper.writelines(minimum_skill_front_markdown_end_of_version(skillfront))


# ============================================================================================================================ #
# Public - Helper function                                                                                                     #
# ============================================================================================================================ #
def minimum_skill_front_markdown_end_of_version(skillfront: MinimumStates) -> list[str]:
    return [
        '# Minimum skill front: End of RuneScape Classic\n\n',
        *stats_menu_markdown({skill: level for skill, (level, _) in skillfront.items()}),
        "\n",
        *requirement_reasons_markdown(skillfront),
        "\n",
        f"*Last updated: {datetime.datetime.now():%d %B %Y - %H:%M:%S}*\n"
    ]


def minimum_skill_front_markdown_end_of_year(update: UpdateInfo, skillfront: MinimumStates) -> list[str]:
    return [
        f'# Minimum skill front: End of {update.date.year}\n\n',
        *stats_menu_markdown({skill: level for skill, (level, _) in skillfront.items()}),
        "\n",
        *requirement_reasons_markdown(skillfront),
        "\n",
        f"*Last updated: {datetime.datetime.now():%d %B %Y - %H:%M:%S}*\n"
    ]


def minimum_skill_front_markdown(update: UpdateInfo, skillfront: MinimumStates) -> list[str]:
    return [
        f'# Minimum skill front: {update.name}\n\n',
        *stats_menu_markdown({skill: level for skill, (level, _) in skillfront.items()}),
        "\n",
        *requirement_reasons_markdown(skillfront),
        "\n",
        f"*Last updated: {datetime.datetime.now():%d %B %Y - %H:%M:%S}*\n"
    ]


def stats_menu_markdown(levels: dict[Skill, int]) -> list[str]:
    """Generate a list of lines that shows the given level overview in markdown files."""
    n_rows_maximum = math.ceil(len(Skill) / 3)
    rows = [['', '', ''] for _ in range(n_rows_maximum)]

    # Insert icons and levels in rows
    for skill, (i, j, icon) in SKILL_ICONS.items():
        if level := levels.get(skill, None):
            rows[i - 1][j - 1] = f"{icon} {level}"

    # Remove empty rows in the bottom on overview - Stop when first non-reducdant line is hit.
    for i in range(len(rows) - 1, -1, -1):
        if rows[i] != ['', '', '']:
            break
        rows.pop(i)

    # Format rows and add header
    return [
        '|     |     |     |\n',
        '| --- | --- | --- |\n',
        *(f"| {col1} | {col2} | {col3} |\n" for (col1, col2, col3) in rows),
    ]


def requirement_reasons_markdown(front: MinimumStates) -> list[str]:
    return [
        '## Goals\n\n',
        '### Column 1\n\n',
        *_requirement_markdown_single_column(1, front),
        '### Column 2\n\n',
        *_requirement_markdown_single_column(2, front),
        '### Column 3\n\n',
        *_requirement_markdown_single_column(3, front),
    ]


# ============================================================================================================================ #
# Private - Helper function                                                                                                    #
# ============================================================================================================================ #
def _update_current_total_level_in_readme(lines: list[str], overview: LevelOverview) -> None:
    """Find and update the 'total-level' line in the README file stored in line."""
    total_level = overview.get_total_level()
    maximum_total_level = max_total_level(CURRENT_INGAME_DATE)

    for i, line in enumerate(lines):
        if TOTAL_LEVEL_PATTERN.match(line):
            print(f"Found total level on line {i + 1}")
            lines[i] = f'- Total level: {total_level} / {maximum_total_level}.\n'
            return

    raise ValueError('Cound not find total level line')


def _update_combat_level_in_readme(readme_lines: list[str], level_overview: LevelOverview) -> None:
    for i, line in enumerate(readme_lines):
        if COMBAT_LEVEL_PATTERN.match(line):
            print(f"Found combat level on line {i + 1}")
            readme_lines[i] = f'- Combat level: {level_overview.get_combat_level()}.\n'
            return

    raise ValueError('Cound not find combat level line')


def _update_current_update_line_in_readme(lines: list[str], update: UpdateInfo, update_window: DateRange) -> None:
    """Update the line in the README that points to the update"""
    linkstring = f"./{urllib.parse.quote(update.path.relative_to(ROOT).as_posix())}"

    for i, line in enumerate(lines):
        if CURRENT_DATE_PATTERN.match(line):
            print(f"Found 'current update' line at {i + 1}")
            lines[i] = f"- [Current date]({linkstring}): {repr(update_window)}.\n"
            return

    raise ValueError("Could not find the 'current date' line in README file")


def _insert_states_in_readme(lines: list[str], overview: LevelOverview) -> list[str]:
    # Find lines where levels menu starts    and ends in README.md file.
    start, end = None, None
    for i, line in enumerate(lines):
        if STATES_MENU_START_PATTERN.match(line):
            assert start is None, "Start has already been found"
            start = i
        if STATES_MENU_END_PATTERN.match(line):
            assert end is None, "End has already been found"
            end = i
    assert start is not None and end is not None, "Missing either start or end."

    # Insert state menu
    before, after = lines[:start + 1], lines[end:]
    state_menu_lines = stats_menu_markdown(overview.levels)

    return before + state_menu_lines + after


def _set_last_updates_line(lines: list[str]) -> None:
    """Update the line which states when the README was last updates"""
    line_index: None | int = None
    for i, line in enumerate(lines):
        if LAST_UPDATES_LINE_PATTERN.match(line):
            assert line_index is None, "line_index is already set"
            line_index = i
    assert line_index is not None, "Last updated line was not found"
    lines[line_index] = f"*Last updates: {datetime.datetime.now():%d %B %Y - %H:%M:%S}*\n"


def _requirement_markdown_single_column(column: int, front: MinimumStates) -> list[str]:
    lines = {}
    for skill, (i, j, icon) in SKILL_ICONS.items():
        if j == column and skill in front:
            level, reason = front[skill]
            lines[i] = f"- {icon} {level}" + (f" - *{reason}*" if reason else "") + "\n"
    return list(lines.values()) + ["\n", ]


if __name__ == '__main__':
    main()
