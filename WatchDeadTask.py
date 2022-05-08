import os

import requests
from dotenv import load_dotenv

from DBHandler import DBHandler
from Message import Message
from UserDB import UserDB

load_dotenv()


def WatchDeadTask(db_id):
    results = db_handler.get_deadline_task(db_id, os.getenv("DEADLINE_LIMIT_DAYS"))
    for idx in range(len(results)):
        requests.post(os.getenv("DISCORD_WEBHOOK"), message.deadLineMessage(results[idx]))


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB()
message = Message(db_handler, user_db,"ようさん")

WatchDeadTask(os.getenv("DB"))
