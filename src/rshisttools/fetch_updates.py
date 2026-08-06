"""Fill the overview file from the Game Update page on the RS3 wiki"""
import json
import requests
from typing import TextIO
from bs4 import BeautifulSoup
from rshisttools.paths import UPDATE_OVERVIEW


HTTP_OK_STATUS_CODE = 200
WIKIROOT = "https://runescape.wiki/"
GAME_UPDATES_HREF = "https://runescape.wiki/w/Game_updates"


def get_updates(out: TextIO) -> None:
    soup = get_content()
    updates = []
    for tables in soup.find_all("table", attrs={'class': 'wikitable'}):
        updates += get_into_table(tables)
    json.dump(updates, out, indent=2)


def get_content() -> BeautifulSoup:
    with requests.get(GAME_UPDATES_HREF) as page:
        if page.status_code != HTTP_OK_STATUS_CODE:
            raise ConnectionError('No connection found')
        return BeautifulSoup(page.text, 'html.parser')


def get_into_table(soup: BeautifulSoup) -> list[dict[str, str]]:
    data = []
    for x in soup.find_all('tr'):
        match x.find_all('td'):
            case []:
                continue
            case [__date, __link]:
                print(date := __date.text)
                data.append({
                    'date': date,
                    'link': WIKIROOT + __link.find('a')['href'],
                    'name': __link.text,
                })
            case _:
                continue
    return data


if __name__ == '__main__':
    with open(UPDATE_OVERVIEW, 'w') as filewrapper:
        get_updates(filewrapper)
