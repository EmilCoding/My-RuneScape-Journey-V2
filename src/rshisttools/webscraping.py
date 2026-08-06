"""Fetch update entries from the RuneScape Game updates wiki page.

This module scrapes the RuneScape Game updates page at
https://runescape.wiki/w/Game_updates and yields raw update entries.
Each entry includes the update title, an absolute wiki URL, and the
published date parsed into ISO 8601 form.
"""
import time
import json
import requests
from bs4 import BeautifulSoup, Tag
from typing import Generator, TypedDict
from rshisttools.dates import date_from_string
from rshisttools.paths import RAW_UPDATES_TABLE_FILE


HTTP_OK_STATUS_CODE = 200
WIKIROOT = "https://runescape.wiki/"
HREF_GAME_UPDATES = "https://runescape.wiki/w/Game_updates"


class UpdateEntry(TypedDict):
    name: str
    href: str
    isodatestring: str


def scrape_and_save_updates_to_table() -> None:
    """Write raw update entries as JSON to a text stream.

    This function fetches updates from the wiki and writes them as JSON into
    :data:`rshisttools.paths.RAW_UPDATES_FILE`.
    """
    updates = list(fetch_updates_from_wikipage())
    with open(RAW_UPDATES_TABLE_FILE, "w", encoding="utf-8") as filewrapper:
        json.dump(updates, filewrapper, indent=2)


def fetch_updates_from_wikipage() -> Generator[UpdateEntry, None, None]:
    """Yield raw update entries scraped from the Game updates wiki page."""
    soup = get_content_from_updates_wikipage()

    for table in soup.find_all("table", attrs={"class": "wikitable"}):
        yield from get_into_table(table)


def get_content_from_updates_wikipage() -> BeautifulSoup:
    """Fetch and parse the RuneScape Game updates wiki page."""
    time.sleep(0.1)
    with requests.get(HREF_GAME_UPDATES) as page:
        if page.status_code != HTTP_OK_STATUS_CODE:
            raise ConnectionError('No connection found')
        return BeautifulSoup(page.text, 'html.parser')


def get_into_table(table: Tag) -> Generator[UpdateEntry, None, None]:
    """Extract update entries from a wiki table element.

    Each row is expected to contain exactly two table cells: one for the date
    and one for the update link. Rows that do not match this shape are skipped.

    The returned entries contain:
        - name: the update title text
        - href: the absolute wiki URL for the update
        - isodatestring: the parsed date in ISO 8601 format
    """
    for row in table.find_all("tr"):
        match row.find_all("td"):
            case [date_cell, link_cell]:
                if (anchor := link_cell.find_next("a")) is None:
                    continue
                yield UpdateEntry(
                    name=link_cell.text.strip(),
                    href=f"{WIKIROOT}{anchor['href']}",
                    isodatestring=date_from_string(date_cell.text).isoformat(),
                )


if __name__ == '__main__':
    for update in fetch_updates_from_wikipage():
        print(update)
