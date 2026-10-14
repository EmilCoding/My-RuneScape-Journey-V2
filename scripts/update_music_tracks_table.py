"""
Fetch the newest music tracks from the RuneScape wiki and append 
them to the music tracks table
"""
import re
import requests
from bs4 import BeautifulSoup
from rshisttools.paths import MUSIC_TRACKS
from rshisttools.dates import date_from_string


WIKI_LINK = 'https://runescape.wiki/w/List_of_music_tracks'

TABLE_HEADER = """
| Id | Title | Unlock hint | Release |
| -- | ----- | ----------- | ------- |
"""

TABLE_PATTERN = re.compile(r"^\| ([0-9]+) \| (.*) \| (.*) \| (.*) \|")
"""Pattern that music tracks are documented in the checklist markdown file.

Groups:
1. Track number (positive integer)
2. Name of the track
3. Unlock hint
4. Release date
"""

# Get last documented music track
with open(MUSIC_TRACKS, 'r') as filewrapper:
    content = filewrapper.readlines()

*_, last_match = filter(None, map(TABLE_PATTERN.match, content))
index_str, name, hint, release_date_string = last_match.groups()

index = int(index_str)
release_date_last_track = date_from_string(release_date_string)
print(f"Last track recorded was: {name}. It released on {release_date_last_track} and was the {index}'th track")


# Get all track released after the last documented music track
with requests.get(WIKI_LINK) as source:
    content = BeautifulSoup(source.content, 'html.parser')
_, *trackinfo_list = content.find('table').find('tbody').find_all('tr')


info_list = []
for tag in trackinfo_list:
    try:
        index = int(tag.get('data-rowid'))
        title_tag, hint_tag, _, __, release_tag, __ = tag.find_all('td')
    
        title = title_tag.text
        hint = hint_tag.text
        release_date = date_from_string(release_tag.text)

        if release_date > release_date_last_track:
            info_list.append((index, title, hint, release_date))
    
    except Exception:
        continue


with open(MUSIC_TRACKS, 'r') as filewrapper:
    file_content = filewrapper.readlines()

# Add sub-header if necessary
if not any(line.startswith('## Unsorted tracks') for line in file_content):
    file_content += ['## Unsorted tracks\n', '\n']

header_index = file_content.index('## Unsorted tracks\n')

if not any(line.startswith(TABLE_HEADER) for line in file_content[header_index:]):
    file_content.append(TABLE_HEADER)


file_content += [
    f"| {index} | {title} | {hint} | {release_date.isoformat()} |\n"
    for index, title, hint, release_date in sorted(info_list, key=lambda x: x[0])
]


if file_content[-1] != '\n':
    file_content.append('\n')


with open(MUSIC_TRACKS, 'w') as filewrapper:
    filewrapper.writelines(file_content)