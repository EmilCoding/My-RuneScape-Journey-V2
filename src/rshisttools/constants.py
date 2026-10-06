"""Load account details defined in the .env file."""
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

@lambda _: _()
def PLAYERNAME():
    """Name of the player's account"""
    if (name := os.getenv("ACCOUNTNAME")) is None:
        raise ValueError('Could not find the field `ACCOUNTNAME` in .env file')
    return name


@lambda _: _()
def ACCOUNT_START_DATE():
    """Start date of the account."""
    if (datestring := os.getenv("ACCOUNTSTART")) is None:
        raise ValueError('Could not find the field `ACCOUNTSTART` in .env file')
    year, month, day = map(int, datestring.split('.'))
    return datetime.date(year, month, day)


if __name__ == '__main__':
    print(f"Player name: {PLAYERNAME}")
    print(f"Start date: {ACCOUNT_START_DATE}")
