"""Load account details defined in the .env file."""
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
PLAYERNAME = os.getenv("ACCOUNTNAME")
ACCOUNT_START_DATE = datetime.date(*map(int, os.getenv("ACCOUNTSTART").split('.')))  # type: ignore


if __name__ == '__main__':
    print(f"Player name: {PLAYERNAME}")
    print(f"Start date: {ACCOUNT_START_DATE}")
