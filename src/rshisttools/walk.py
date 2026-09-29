"""Helpers for discovering RuneScape update files from the repository layout.

This module scans the project tree for markdown update notes that follow the
repository's naming convention and exposes helpers for finding the current
update window, counting updates, and filtering updates by date or year.
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


class DateRange(NamedTuple):
    """Represents a start/end date range for a set of updates."""
    start: datetime.date
    end: datetime.date

    def ___str__(self) -> str:
        assert self.start <= self.end, "Start must come before end"
        return "DateRange({:%d %B %Y}, {:%d %B %Y})".format(self.start, self.end)

    def __repr__(self) -> str:
        """Return a human-readable representation of the date range."""
        assert self.start <= self.end, "Start must come before end"
        return "({:%d %B %Y} -- {:%d %B %Y})".format(self.start, self.end)


class WalkOptions(TypedDict):
    """Optional filters accepted by :func:`walk_updates`."""
    start: NotRequired[datetime.date]
    end: NotRequired[datetime.date]
    year: NotRequired[int]


@dataclass
class UpdateInfo:
    """Represents a single update note parsed from its filename."""
    name: str
    path: pathlib.Path
    date: datetime.date

    def __repr__(self) -> str:
        """Return a human-readable description of the update."""
        return f"{self.date} - {self.name}"

    def get_date(self) -> datetime.date:
        return self.date

    def as_url(self) -> str:
        return f"./{urllib.parse.quote(self.path.relative_to(ROOT).as_posix())}"

    def __lt__(self, other: UpdateInfo | datetime.date) -> bool:
        if isinstance(other, UpdateInfo):
            other = other.date
        return self.date < other

    def __gt__(self, other: UpdateInfo | datetime.date) -> bool:
            if isinstance(other, UpdateInfo):
                other = other.date
            return self.date > other


INCOMPLETE_GOALS_PATTERN = re.compile(r'^\s*- \[ \] (.*)\n?$')
UPDATE_FILENAME_PATTERN = re.compile(r'^(\d{4})\.(\d{2})\.(\d{2}) - (?:Update )?(.*)\.md$')


def current_ingame_date() -> datetime.date:
    """Return the most relevant in-game date for the current repository state."""
    if updates_in_root := get_updates(with_root=True):
        return min(updates_in_root, key=UpdateInfo.get_date).date

    # No files in root - Take last completed
    return max(get_updates(with_completed=True, with_partially_completed=True), key=UpdateInfo.get_date).date


def updates_in_folder(folder: pathlib.Path, /, with_subdir: bool = True, **options: Unpack[WalkOptions]) -> int:
    """Return the number of update files located in a folder."""
    assert folder.is_dir(), "Provided path is not a directory"
    return sum(1 for _ in walk_updates(folder, with_subdir, **options))


def total_updates(**options: Unpack[WalkOptions]) -> int:
    """Count updates in a given year or across the full repository tree."""
    return sum(1 for _ in get_updates(with_all=True, **options))


def get_updates(
    with_all: bool = False,
    with_root: bool = False,
    with_completed: bool = False,
    with_partially_completed: bool = False,
    with_future: bool = False,
    **walk_options: Unpack[WalkOptions]
) -> Iterator[UpdateInfo]:
    """Get

    Args:
        with_all (bool, optional): If True, the include all files. Defaults to False.
        with_root (bool, optional): If True, the include root files. Defaults to False.
        with_completed (bool, optional): If True, the include completed goals. Defaults to False.
        with_partially_completed (bool, optional): If True, the include partially completed goals. Defaults to False.
        with_future (bool, optional): If True, the include future. Defaults to False.
    """
    with_root = with_all or with_root
    with_completed = with_all or with_completed
    with_partially_completed = with_all or with_partially_completed
    with_future = with_all or with_future

    updates: list[Iterator[UpdateInfo]] = []
    if with_root:
        updates.append(walk_updates(ROOT, with_subdir=False, **walk_options))
    if with_completed:
        updates.append(walk_updates(COMPLETED_GOALS, with_subdir=True, **walk_options))
    if with_partially_completed:
        updates.append(walk_updates(PARTIALLY_COMPLETED, with_subdir=True, **walk_options))
    if with_future:
        updates.append(walk_updates(FUTURE_GOALS, with_subdir=True, **walk_options))

    return itertools.chain(*updates)


def walk_updates(
    folder: pathlib.Path,
    with_subdir: bool = True,
    **options: Unpack[WalkOptions]
) -> Iterator[UpdateInfo]:
    """Return an iterator yielding all updates in a given folder.

    The name of the file is used to determine if the file is an update file,
    if it matches the regex pattern 'UPDATE_FILENAME_PATTERN'. From the path,
    the update name and date can be extracted and returned.

    Args:
        folder: Directory to scan for update files.
        with_subdir: If True, the files in subfolders are also included. Defaults to True.
        start: Optional lower bound for the update date.
        end: Optional upper bound for the update date.
        year: Optional year filter.

    Returns:
        An iterator over all updates in folder as `UpdateInfo` objects.
    """
    filepaths = _all_subfiles(folder, with_subdir)
    updates = filter(None, map(_extract_updateinfo, filepaths))

    # Add a filter to the walk from 'walkoptions'
    if (start := options.get('start', None)):
        updates = filter(lambda x: x.date >= start, updates)
    if (end := options.get('end', None)):
        updates = filter(lambda x: x.date <= end, updates)
    if (year := options.get('year', None)):
        updates = filter(lambda x: x.date.year == year, updates)

    return updates


def get_current_update_window() -> tuple[UpdateInfo, DateRange]:
    """Return the active update file and the date range it covers.

    The returned tuple contains the current update file path and a start/end
    date pair that describes the current update window. The exact shape depends
    on whether the repository root contains zero, one, or multiple update files.
    """
    match updates := list(walk_updates(ROOT, with_subdir=False)):
        case []:
            # No updates found in ROOT
            last_completed_update = max(get_updates(with_completed=True, with_partially_completed=True), key=UpdateInfo.get_date)
            next_update = min(get_updates(with_future=True), key=UpdateInfo.get_date)
            return last_completed_update, DateRange(last_completed_update.date, next_update.date)

        case [update, ]:
            # 1 updates found in ROOT
            next_update = min(get_updates(with_future=True), key=UpdateInfo.get_date)
            return update, DateRange(update.date, next_update.date)

        case _:
            # Many files found in ROOT
            first_update = min(updates, key=UpdateInfo.get_date)
            last_update = max(updates, key=UpdateInfo.get_date)
            return first_update, DateRange(first_update.date, last_update.date)


def _all_subfiles(root: pathlib.Path, with_subdir: bool) -> Generator[pathlib.Path, None, None]:
    """Yield every file beneath a root directory. """
    if not with_subdir:
        (folder, _, files), *_ = os.walk(root)
        yield from map(pathlib.Path(folder).joinpath, files)
        return

    # Walk through all subdirectories
    for folder, _, files in os.walk(root):
        yield from map(pathlib.Path(folder).joinpath, files)


def _extract_updateinfo(filepath: pathlib.Path) -> None | UpdateInfo:
    """Parse a file path into an UpdateInfo object when it matches the naming convention."""
    if not (__match := UPDATE_FILENAME_PATTERN.match(filepath.name)):
        return None

    date = datetime.date(
        year=int(__match.group(1)),
        month=int(__match.group(2)),
        day=int(__match.group(3)),
    )
    name = __match.group(4)
    return UpdateInfo(name, filepath, date)


CURRENT_INGAME_DATE = current_ingame_date()
"""Ingame date based on the file structure at "compile time"."""


if __name__ == '__main__':
    update, window = get_current_update_window()
    *_, last_update = walk_updates(FUTURE_GOALS)

    print("Update statistics:")
    print("==================")
    print(f"Current date window: {window} ({update.name})")
    print(f"Updates completed: {updates_in_folder(COMPLETED_GOALS)}")
    print(f"Updates partially completed: {updates_in_folder(PARTIALLY_COMPLETED)}")
    print(f"Updates in total: {total_updates()}")
    print(f"Updates in this year: {total_updates(year=update.date.year)}")
    print("Last update file is dated to {:%d %B %Y}".format(last_update.date))
    print(f"Updates yet to be completed: {updates_in_folder(FUTURE_GOALS)}")
    print(f"Days since last update file {(datetime.date.today() - last_update.date).days} days")
