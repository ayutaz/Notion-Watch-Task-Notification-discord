import os

import requests
from dotenv import load_dotenv

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB

load_dotenv()


def WatchDeadTask(db_id):
    results = db_handler.get_deadline_task(db_id, deadline_limit_days)
    for idx in range(len(results)):
        requests.post(os.getenv("DISCORD_WEBHOOK"), message.deadLineMessage(results[idx]))


deadline_limit_days = os.getenv("DEADLINE_LIMIT_DAYS") or "3"
db_handler = TaskDBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB(os.getenv("USERS"))
message = Message(db_handler, user_db, os.getenv("CONFIRM_USER"), deadline_limit_days)

WatchDeadTask(os.getenv("DB"))
