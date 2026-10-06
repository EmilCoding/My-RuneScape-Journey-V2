"""Helpers for discovering RuneScape update files from the repository layout.

This module scans the project tree for markdown update notes that follow the
repository's naming convention and exposes helpers for finding the current
update window, counting updates, and filtering updates by date or year.

Most important functions:

- ´get_updates´ : Access all updates selectively by providing flags to the caller.
- ´current_ingame_date´ : Calculates the current in-game date from the project structure.
- ´updates_in_folder´ : Count the number of updates in a given folder.
- ´total_updates´ : Count the number of updates in a given folder.
- ´get_current_update_window´ : Get update window of active updates.
"""
import os
import re
import pathlib
import datetime
import itertools
import urllib.parse
from dataclasses import dataclass
from typing import Generator, Iterator, NamedTuple, NotRequired, TypedDict, Unpack

from rshisttools.paths import ROOT, FUTURE_GOALS, COMPLETED_GOALS, PARTIALLY_COMPLETED


UPDATE_FILENAME_PATTERN = re.compile(r'^(\d{4})\.(\d{2})\.(\d{2}) - (?:Update )?(.*)\.md$')
"""Regex pattern that matches update file names and extracts day, month, year, and update name.

Capture groups:
  1. Year as a four digit integer
  2. Month as a two digit integer with possible leading zero.
  3. Day as a two digit integer with a possible leading zero.
  4. Name of the update as a string
"""

INCOMPLETE_GOALS_PATTERN = re.compile(r'^\s*- \[ \] (.*)\n?$')


class WalkOptions(TypedDict):
    """Optional keyword arguments for walking function."""
    start: NotRequired[datetime.date]
    end: NotRequired[datetime.date]
    year: NotRequired[int]


class DateRange(NamedTuple):
    """Represents an interval of dates. None is interpreted as unbound"""
    start: None | datetime.date
    end: None | datetime.date

    def ___str__(self) -> str:
        start_str = 'None' if self.start is None else f"{self.start:%d %B %Y}"
        end_str = 'None' if self.end is None else f"{self.end:%d %B %Y}"
        return f"DateRange({start_str}, {end_str})"

    def __repr__(self) -> str:
        """Return a human-readable representation of the date range."""
        start_str = '-inf' if self.start is None else f"{self.start:%d %B %Y}"
        end_str = 'inf' if self.end is None else f"{self.end:%d %B %Y}"
        return f"({start_str}, {end_str})"

    def __contains__(self, key: object) -> bool:
        """Magic method of the ´in´ keyword. Check if ´date´ is in interval."""
        if not isinstance(key, datetime.date | datetime.datetime):
            return False
        if not (self.start and self.start <= key):
            return False
        if not (self.end and key <= self.end):
            return False
        return True


@dataclass(frozen=True)
class UpdateInfo:
    """Represents a single update file."""
    name: str
    """Name of the update."""
    path: pathlib.Path
    """Path to the update file."""
    date: datetime.date
    """Date of the update."""

    def __repr__(self) -> str:
        """Return a human-readable description of the update."""
        return f"{self.date} - {self.name}"

    def get_date(self) -> datetime.date:
        return self.date

    def as_url(self) -> str:
        """Return path as an url string. Can be used in markdown files to point to file."""
        return f"./{urllib.parse.quote(self.path.relative_to(ROOT).as_posix())}"

    def __lt__(self, other: UpdateInfo | datetime.date) -> bool:
        """Magic method implementing functionallity of the ´<´ keyword."""
        if isinstance(other, UpdateInfo):
            other = other.date
        return self.date < other

    def __gt__(self, other: UpdateInfo | datetime.date) -> bool:
        """Magic method implementing functionallity of the ´>´ keyword."""
        if isinstance(other, UpdateInfo):
            other = other.date
        return self.date > other


def get_updates(
    with_all: bool = False,
    with_root: bool = False,
    with_completed: bool = False,
    with_partially_completed: bool = False,
    with_future: bool = False,
    **walk_options: Unpack[WalkOptions]
) -> Iterator[UpdateInfo]:
    """Access all updates selectively by providing flags to the caller.

    Args:
        with_all (bool, optional): If True, include all updates in project. Defaults to False.
        with_root (bool, optional): If True, the include updates in root. Defaults to False.
        with_completed (bool, optional): If True, include all completed updates. Defaults to False.
        with_partially_completed (bool, optional): If True, include all partially completed updates.
          Defaults to False.
        with_future (bool, optional): If True, include all future updates. Defaults to False.
    """
    updates: list[Iterator[UpdateInfo]] = []
    if with_all or with_root:
        updates.append(get_updates_from_folder(ROOT, with_subdir=False, **walk_options))
    if with_all or with_completed:
        updates.append(get_updates_from_folder(COMPLETED_GOALS, with_subdir=True, **walk_options))
    if with_all or with_partially_completed:
        updates.append(get_updates_from_folder(PARTIALLY_COMPLETED, with_subdir=True, **walk_options))
    if with_all or with_future:
        updates.append(get_updates_from_folder(FUTURE_GOALS, with_subdir=True, **walk_options))

    return itertools.chain(*updates)


def current_ingame_date() -> datetime.date:
    """Return the most relevant in-game date for the current repository state."""
    return get_current_update().date


def get_updates_from_folder(
    folder: pathlib.Path,
    with_subdir: bool = True,
    **options: Unpack[WalkOptions]
) -> Iterator[UpdateInfo]:
    """Return an iterator yielding all updates in a given folder.

    The name of the file is used to determine if the file is an update file,
    if it matches the regex pattern 'UPDATE_FILENAME_PATTERN'. From the path,
    the update name and date can be extracted and returned.

    Args:
        folder (pathlib.Path): Starting point for the recursive walk.
        with_subdir (bool, optional): If True, the files in subfolders are also included. Defaults to True.
        start (datetime.date, optional): If provided, all update date before given date are excluded.
        end: (datetime.date, optional): If provided, all update date after given date are excluded.
        year (int, optional): If provided, only include updates in the given year.

    Returns:
        Iterator[UpdateInfo]: An iterator providing `UpdateInfo` instances for all updates in folder.
    """
    filepaths = all_subfiles(folder, with_subdir)
    updates = filter(None, map(extract_updateinfo, filepaths))

    # Add a filter to the walk from 'walkoptions'
    if (start := options.get('start', None)):
        updates = filter(lambda x: x.date >= start, updates)
    if (end := options.get('end', None)):
        updates = filter(lambda x: x.date <= end, updates)
    if (year := options.get('year', None)):
        updates = filter(lambda x: x.date.year == year, updates)

    return updates


def all_subfiles(root: pathlib.Path, with_subdir: bool = True) -> Generator[pathlib.Path, None, None]:
    """Yield the paths of all files in the given directory.

    Args:
        root (pathlib.Path): Path to the folder in question.
        with_subdir (bool, optional): If True, all files in the subfolders are also included.
          Default is True.

    Yields:
        pathlib.Path: Path to subfiles.
    """
    walk_triplets = os.walk(root) if with_subdir else [next(os.walk(root)), ]

    for folder, _, files in walk_triplets:
        yield from map(pathlib.Path(folder).joinpath, files)


def extract_updateinfo(filepath: pathlib.Path) -> None | UpdateInfo:
    """Parse a file path into an UpdateInfo object when it matches the naming convention. If not, return None"""
    if (match := UPDATE_FILENAME_PATTERN.match(filepath.name)) is None:
        return None
    year_str, month_str, day_str, name = match.groups()
    date = datetime.date(year=int(year_str), month=int(month_str), day=int(day_str))
    return UpdateInfo(name, filepath, date)


def updates_in_folder(folder: pathlib.Path, with_subdir: bool = True, **options: Unpack[WalkOptions]) -> int:
    """Return the number of update files located in a folder."""
    return sum(1 for _ in get_updates_from_folder(folder, with_subdir, **options))


def count_updates(
    with_all: bool = False,
    with_root: bool = False,
    with_completed: bool = False,
    with_partially_completed: bool = False,
    with_future: bool = False,
    **walk_options: Unpack[WalkOptions]
) -> int:
    updates = get_updates(with_all, with_root, with_completed, with_partially_completed, with_future, **walk_options)
    return sum(1 for _ in updates)


def get_current_update() -> UpdateInfo:
    """Get current update."""
    if updates := list(get_updates(with_all=True)):
        return min(updates, key=lambda x: x.date)

    if updates := list(get_updates(with_partially_completed=True, with_completed=True)):
        return max(updates, key=lambda x: x.date)

    if updates := list(get_updates(with_future=True)):
        return min(updates, key=lambda x: x.date)

    raise FileNotFoundError('No files in project folder.')


def get_next_update() -> None | UpdateInfo:
    """Get the next update if it exists. None if no future updates exists."""
    if updates := list(get_updates(with_root=True)):
        return max(updates, key=lambda x: x.date)

    if updates := list(get_updates(with_future=True)):
        return min(updates, key=lambda x: x.date)

    return None


def get_current_update_window() -> DateRange:
    return DateRange(
        current_ingame_date(),
        update.date if (update := get_next_update()) else None,
    )


if __name__ == '__main__':
    current_update = get_current_update()
    assert (next_update := get_next_update()) is not None
    date_range = get_current_update_window()

    print("Update statistics:")
    print("==================")
    print(f"Current date window: {date_range} ({current_update.name})")
    print(f"Updates completed: {count_updates(with_completed=True)}")
    print(f"Updates partially completed: {count_updates(with_partially_completed=True)}")
    print(f"Updates in total: {count_updates(with_all=True)}")
    print(f"Updates in this year: {count_updates(with_all=True, year=current_update.date.year)}")
    print("Last update file is dated to {:%d %B %Y}".format(next_update.date))
    print(f"Updates yet to be completed: {count_updates(with_future=True)}")
    print(f"Days since last update file {(datetime.date.today() - next_update.date).days} days")
