"""
Module to extract and handle goals from the update files
"""
import re


GOALS_PATTERN = re.compile(r'- \[([ , x])\] (?:\(!Optional\) )?(.*)')
"""Regex pattern that matches any goal/optional goal both complete and incomplete
- [ ] Goals name
- [x] Goals name
- [ ] (!Optional) Goals name
- [x] (!Optional) Goals name

Capture groups:
1. Completion status. ' ' represents non-complete. 'x' represents completed.
2. Description.
"""


REQUIRED_SKILL_REQUIREMENT_PATTERN = re.compile(r'^- \[([ ,x])\] (\d+) (\w+)(?: - \*(.*)\*)?$')
"""Regex pattern that matches any required skill goal complete or not.

Capture groups:
1. Completion mark
2. Level as a string
3. Desciption
4. Optional description
"""


OPTIONAL_SKILL_REQUIREMENT_PATTERN = re.compile(r'^- \[([ ,x])\] \(!Optional\) (\d+) (\w+)(?: - \*(.*)\*)?$')
"""Regex pattern that matches any optional skill goal complete or not.

Capture groups:
1. Completion mark
2. Level as a string
3. Desciption
4. Optional description
"""


