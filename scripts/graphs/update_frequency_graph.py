"""
Make a histogram over the 
"""
from typing import Counter
import matplotlib.pyplot as plt 
from rshisttools.walk import get_updates
from rshisttools.paths import GRAPHICS_FOLDER


WEEKS_PER_YEAR = 52
update_year_data = Counter(update.date.year for update in get_updates(with_all=True))


fig, ax = plt.subplots()

years = sorted(update_year_data)
update_count = [
    count
    for _, count in sorted(update_year_data.items(), key=lambda x: x[0])
]

ax.stem(years, update_count, '-o')
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

fig.savefig(GRAPHICS_FOLDER.joinpath('number-of-updates-per-year.png'))
plt.show()
