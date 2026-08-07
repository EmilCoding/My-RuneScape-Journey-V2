"""
Module contains functionallity to generate plots automatically.
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import rshisttools.dates as dates

from typing import Counter
from rshisttools.runemetrics_api import get_ingame_overview
from rshisttools.walk import get_updates, current_ingame_date
from rshisttools.dates import max_level
from rshisttools.skillfront import skill_front_history, total_level


WEEKS_PER_YEAR = 52
CURRENT_INGAME_DATE = current_ingame_date()
FRONT_HISTORY = skill_front_history(CURRENT_INGAME_DATE)

RED = "#FF0000"
BLUE = "#0000FF"
GREEN = "#0C6F0C"


def updates_histogram():
    updates_per_year = Counter(update.date.year for update in get_updates(with_all=True))
    years = sorted(updates_per_year)
    update_count = [count for _, count in sorted(updates_per_year.items(), key=lambda x: x[0])]

    fig, ax = plt.subplots()

    ax.axvline(current_ingame_date().year, color='orange', label='My current year')
    ax.stem(years, update_count, 'o', basefmt='', label='Update count')

    ax.set_ylabel('Number of updates')
    ax.set_xticks(years, map(str, years), rotation=45)
    ax.set_title('Update count of RuneScape 3 per year')
    ax.set_xlim(min(years) - 1, max(years) + 1)
    ax.set_ylim(0,)

    # Create a second y-axis to show update frequency
    ax2 = ax.twinx()
    ax2.set_ylabel('Update frequency per week')
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(ax.get_yticks())
    ax2.set_yticklabels([f"{x / WEEKS_PER_YEAR:0.1f}" for x in ax2.get_yticks()])

    ax.legend()
    return fig


def total_level_evolution():
    """
    Make a plot that shows the evolution of max total level
    as well as the total level of the minimum-skill-front.

    Future work:
    - Add labels to dates where skill caps are raised from 99 to 110
    - Add labels to dates where skill caps are raised from 99 to 120
    """
    in_game_date = current_ingame_date()
    history = skill_front_history(in_game_date)[1:]

    dates_array = np.array([update.date for (update, _) in history], dtype=datetime.date)
    minimum_total_level = np.array([total_level(front) for (_, front) in history])
    maximum_total_level = np.array([dates.max_total_level(update.date) for (update, _) in history])
    maximum_total_level_lookup = {date: level for date, level in zip(dates_array, maximum_total_level)}

    fig, ax = plt.subplots()

    ax.plot(dates_array, maximum_total_level, color=RED, label='Maximum total level')
    ax.plot(dates_array, minimum_total_level, color=BLUE, label='Minimum total level')
    ax.set_ylim(0, 1.10 * maximum_total_level[-1])

    def filterfunc(date: datetime.date) -> bool:
        return date <= in_game_date and date != dates.GAME_RELEASE_DAY

    ax.text(
        dates.GAME_RELEASE_DAY,
        maximum_total_level_lookup[dates.GAME_RELEASE_DAY],
        "Game release",
        va='top',
        ha='left',
    )
    ax.plot(dates.GAME_RELEASE_DAY, maximum_total_level[0], 'x', color=GREEN)
    for skill, date in dates.SKILL_RELEASE_DAYS.items():
        if not filterfunc(date):
            continue
        y = maximum_total_level_lookup[date]
        ax.text(date, y, skill, va='top', ha='left')
    ax.plot(
        [date for date in dates.SKILL_RELEASE_DAYS.values() if filterfunc(date)],
        [maximum_total_level_lookup[date] for date in dates.SKILL_RELEASE_DAYS.values() if filterfunc(date)],
        'x',
        color=GREEN
    )

    ax.legend(loc='upper left')
    ax.set_title('Evolution of max total level and minimum-skill-front')
    ax.set_xlabel('Time')
    ax.set_ylabel('Total level')

    # Add a plot in the left corner of the plot
    left, bottom, width, height = [0.65, 0.2, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.plot(dates_array, minimum_total_level / maximum_total_level)
    ax2.set_title('Percentage of total level', fontsize=10)
    ax2.tick_params('x', rotation=45, labelsize=8)
    ax2.set_yticks(ax2.get_yticks(), [f"{100 * x:0.0f}%" for x in ax2.get_yticks()], size=8)
    ax2.grid(True)

    return fig


def skill_distribution():
    *_, (_, skill_front) = FRONT_HISTORY
    my_levels = get_ingame_overview(CURRENT_INGAME_DATE)

    skills = list(my_levels.levels)
    level_classes = {
        'My levels': list(my_levels.levels.values()),
        'Max level': [max_level(skill, CURRENT_INGAME_DATE) for skill in skills],
        'Minimum skill front': [level for level, _ in skill_front.values()],
    }

    fig, ax = plt.subplots()

    ax.bar(skills, level_classes['Max level'], color=RED, label='Max level')
    ax.bar(skills, level_classes['My levels'], color=BLUE, label='My levels')
    ax.bar(skills, level_classes['Minimum skill front'], color=GREEN, label='Minimum skill front')

    ax.set_ylabel('Level')
    ax.set_xticks(skills)
    ax.set_xticklabels(labels=skills, rotation=45, size=10, ha='right')
    ax.legend(bbox_to_anchor=(0.5, 1.10), loc='upper center', ncols=3)

    fig.tight_layout()
    return fig


if __name__ == '__main__':
    # fig1 = updates_histogram()
    # fig2 = total_level_evolution()
    fig3 = skill_distribution()
    plt.show()
