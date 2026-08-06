#type: ignore
"""
Make a plot that shows the evolution of max total level
as well as the total level of the minimum-skill-front.

Future work:
- Add labels to dates where skill caps are raised from 99 to 110
- Add labels to dates where skill caps are raised from 99 to 120
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt

import rshisttools.dates as dates
from rshisttools.paths import GRAPHICS_FOLDER
from rshisttools.walk import current_ingame_date
from rshisttools.skillfront import skill_front_history, total_level


MAXIMUM_CURVE_COLOUR = "#FF0000"
MINIMUM_CURVE_COLOUR = "#0000FF"
SKILL_RELEASE_COLOUR = "#063A06"


in_game_date = current_ingame_date()
history = skill_front_history(in_game_date)[1:]

dates_array = np.array([update.date for (update, _) in history], dtype=datetime.date)
minimum_total_level = np.array([total_level(front) for (_, front) in history])
maximum_total_level = np.array([dates.max_total_level(update.date) for (update, _) in history])

minimum_total_level_lookup = {date: level for date, level in zip(dates_array, minimum_total_level)}
maximum_total_level_lookup = {date: level for date, level in zip(dates_array, maximum_total_level)}


fig, ax = plt.subplots()

ax.plot(dates_array, maximum_total_level, color=MAXIMUM_CURVE_COLOUR, label='Maximum total level')
ax.plot(dates_array, minimum_total_level, color=MINIMUM_CURVE_COLOUR, label='Minimum total level')
ax.set_ylim(0, 1.10*maximum_total_level[-1])


def filterfunc(date: datetime.date) -> bool:
    return date <= in_game_date and date != dates.GAME_RELEASE_DAY


ax.text(dates.GAME_RELEASE_DAY,
        maximum_total_level_lookup[dates.GAME_RELEASE_DAY],
        "Game release",
        va='top',
        ha='left',
)
ax.plot(dates.GAME_RELEASE_DAY, maximum_total_level[0], 'x', color=SKILL_RELEASE_COLOUR)
for skill, date in dates.SKILL_RELEASE_DAYS.items():
    if not filterfunc(date):
        continue
    y = maximum_total_level_lookup[date]
    ax.text(date, y, skill, va='top', ha='left')
ax.plot(
    [date for date in dates.SKILL_RELEASE_DAYS.values() if filterfunc(date)],
    [maximum_total_level_lookup[date] for date in dates.SKILL_RELEASE_DAYS.values() if filterfunc(date)],
    'x',
    color=SKILL_RELEASE_COLOUR
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
ax2.set_yticks(ax2.get_yticks(), [f"{100*x:0.0f}%" for x in ax2.get_yticks()], size=8)
ax2.grid(True)


fig.savefig(GRAPHICS_FOLDER.joinpath('total_level_evolution.png'))

plt.show()
