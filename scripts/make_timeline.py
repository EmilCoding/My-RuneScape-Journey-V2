import numpy as np
import matplotlib.pyplot as plt

from rshisttools.dates import GAME_RELEASE_DAY
from rshisttools.walk import get_updates, current_ingame_date


CURRENT_INGAME_DATE = current_ingame_date()


updates = sorted(get_updates(with_partially_completed=True))
dates = np.array([update.date for update in updates])
names = np.array([update.name for update in updates])


fig, ax = plt.subplots(figsize=(8.8, 4), layout="constrained")

ax.plot(dates, np.zeros_like(dates), 'o')
ax.plot([GAME_RELEASE_DAY, updates[-1].date], [0, 0], color='black')
ax.set_ylim(-3, 3)

# Set release day
ax.axvline(GAME_RELEASE_DAY, linestyle='--', color='blue', label='Game release day')


# Set current day
ax.axvline(CURRENT_INGAME_DATE, linestyle='--', color='blue', label='Current ingame date')


for i, update in enumerate(updates):
    is_upper = i % 2
    height = 1 if is_upper else -1

    string = name if len(name := update.name) < 13 else (name[:10] + '...')
    ax.plot([update.date, update.date], [0, height], '--k')
    ax.text(update.date,
            height,
            string,
            rotation=45,
            fontsize=8,
            horizontalalignment='left' if i % 2 == 0 else 'right',
            verticalalignment='baseline' if i % 2 == 0 else 'top',
    )


plt.show()
