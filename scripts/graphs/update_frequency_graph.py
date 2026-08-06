"""
Make a histogram over the 
"""
import matplotlib.pyplot as plt 
from typing import Counter
from rshisttools.paths import GRAPHICS_FOLDER
from rshisttools.walk import get_updates, current_ingame_date


WEEKS_PER_YEAR = 52
updates_per_year = Counter(update.date.year for update in get_updates(with_all=True))

years = sorted(updates_per_year)
update_count = [count for _, count in sorted(updates_per_year.items(), key=lambda x: x[0])]


fig, ax = plt.subplots()

ax.stem(years, update_count, 'o', basefmt='', label='Update count')
ax.axvline(current_ingame_date().year, color='orange', label='My current year')

ax.set_ylabel('Number of updates')
ax.set_xticks(years, map(str, years), rotation=45)
ax.set_title('Update count of RuneScape 3 per year')
ax.set_xlim(min(years)-1, max(years)+1)
ax.set_ylim(0,)

# Create a second y-axis
ax2 = ax.twinx()
ax2.set_ylabel('Update frequency per week')
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks(ax.get_yticks())
ax2.set_yticklabels([f"{x / WEEKS_PER_YEAR:0.1f}" for x in ax2.get_yticks()])

ax.legend()
fig.savefig(GRAPHICS_FOLDER.joinpath('number-of-updates-per-year.png'))
plt.show()
