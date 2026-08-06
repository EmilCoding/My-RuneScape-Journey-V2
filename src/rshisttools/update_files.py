"""Create missing future update files from scraped wiki data.

This module reads raw update entries from the saved JSON table file,
compares their dates against the latest update already present in the
future goals folder tree, and creates new markdown files for any updates
that are newer than the existing future goal files.
"""

import re
import json
import pathlib
import datetime


from rshisttools.walk import get_updates
from rshisttools.webscraping import UpdateEntry
from rshisttools.paths import FUTURE_GOALS, RAW_UPDATES_TABLE_FILE, TEMPLATE_FILE


HEADER_LINE_PATTERN = re.compile("# <update-name> - <date>")
UPDATE_LINK_LINE = re.compile(r'\[Update post\]\(...\)')


def make_missing_update_files() -> None:
    """Generate any missing future-update markdown files.

    This function reads the raw update entries from
    :data:`rshisttools.paths.RAW_UPDATES_TABLE_FILE`, then compares each
    update date against the latest existing future update from
    :func:`rshisttools.walk.get_updates` with ``with_future=True``.

    Any scraped update dated after the latest existing future update is
    rendered from the template and written into the appropriate year folder.
    """
    last_update_date_in_future_folder = max(update.date for update in get_updates(with_future=True))

    # Load updates from `RAW_UPDATES_TABLE_FILE`
    with open(RAW_UPDATES_TABLE_FILE, 'r') as filewrapper:
        updates = map(UpdateEntry, json.load(filewrapper))  # type: ignore[arg-type]

    for update in updates:
        name = update['name'].replace(':', ' ')
        link = update['href']
        date = datetime.date.fromisoformat(update['isodatestring'])

        if date <= last_update_date_in_future_folder:
            continue  # Years have already been completed

        filepath, lines = make_update_file(name, link, date, get_folderpath(date.year))
        with open(filepath, 'w') as filewrapper:
            filewrapper.writelines(lines)

    print(F"The {FUTURE_GOALS.name} folder is up-to-date")


# Read the template file and store in `_TEMPLATE_FILE_LINES.
# Please use the `get_template_file_files` method to get a copy to not contain the `TEMPLATE_FILE` variable.
with open(TEMPLATE_FILE, 'r') as filewrapper:
    _TEMPLATE_FILE_LINES = filewrapper.readlines()


def get_template_file_files() -> list[str]:
    """Return a copy of the loaded template file lines.

    The template file is read once at module import time into
    ``_TEMPLATE_FILE_LINES``. This helper returns a fresh copy so callers may
    modify the returned lines without mutating the shared template cache.
    """
    return _TEMPLATE_FILE_LINES.copy()


def get_folderpath(year: int) -> pathlib.Path:
    """Return the destination folder path for the given year.

    If a folder for the exact year exists directly under ``FUTURE_GOALS``, it
    is returned. Otherwise, the function ensures a ``later years/<year>`` folder
    exists and returns that path.
    """
    if (folderpath := FUTURE_GOALS.joinpath(year.__str__())).exists():
        return folderpath
    if not (folderpath := FUTURE_GOALS.joinpath('later years', year.__str__())).exists():
        folderpath.mkdir()
    return folderpath


def make_update_file(
    name: str,
    link: str,
    date: datetime.date,
    folderpath: pathlib.Path,
) -> tuple[pathlib.Path, list[str]]:
    """Create the content and target path for a new update markdown file.

    Parameters:
        name: The URL-quoted update title used in the file name and link text.
        link: The absolute wiki URL for the update.
        date: The parsed update date used for the filename and header.
        folderpath: The destination folder where the file should be created.

    Returns:
        A tuple containing the file path and the rendered list of lines.
    """
    lines = get_template_file_files()
    datestring = (lambda x: x[1:] if x[0] == '0' else x)(f"{date:%d %B &Y}")

    # Generate file name
    filepath = folderpath.joinpath(f"{date:%Y.%m.%d} - {name}.md")

    # Find and replace lines
    set_header, set_update = False, False
    for i, line in enumerate(lines):
        if HEADER_LINE_PATTERN.match(line):
            set_header = True
            lines[i] = f"# {name} - {datestring}\n"
        if UPDATE_LINK_LINE.match(line):
            set_update = True
            lines[i] = f"[{name}]({link})\n"
    assert set_header and set_update

    return filepath, lines


if __name__ == '__main__':
    make_missing_update_files()
