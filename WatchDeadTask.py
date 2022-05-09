import os

import requests
from dotenv import load_dotenv

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB

load_dotenv()


def WatchDeadTask(db_id):
    results = db_handler.get_deadline_task(db_id, os.getenv("DEADLINE_LIMIT_DAYS"))
    for idx in range(len(results)):
        requests.post(os.getenv("DISCORD_WEBHOOK"), message.deadLineMessage(results[idx]))


db_handler = TaskDBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB()
message = Message(db_handler, user_db, os.getenv("CONFIRM_USER"))

WatchDeadTask(os.getenv("DB"))
