import os

import requests
from dotenv import load_dotenv

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB

load_dotenv()


def WatchTaskStatus():
    db = db_handler.get_change_history()
    for task_result in db:
        if task_result is not None:
            if db_handler.is_task_status_confirm_from_doing(task_result):
                requests.post(os.getenv("DISCORD_WEBHOOK"), message.confirm_message(task_result))
            elif db_handler.is_task_status_doing_from_confirm(task_result):
                requests.post(os.getenv("DISCORD_WEBHOOK"), message.fb_message(task_result))


db_handler = TaskDBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB(os.getenv("USERS"))
message = Message(db_handler, user_db, os.getenv("CONFIRM_USER"))

WatchTaskStatus()
