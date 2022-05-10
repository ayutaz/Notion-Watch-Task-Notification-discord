import os

import requests
from dotenv import load_dotenv

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB

load_dotenv()


def WatchTaskStatus():
    db = db_handler.get_change_history(os.getenv("GET_HISTORY_MINUS"))
    for task_result in db:
        if task_result is not None:
            if db_handler.task_status(task_result) == '確認依頼':
                requests.post(os.getenv("DISCORD_WEBHOOK"), message.confirm_message(task_result))
            elif db_handler.task_status(task_result) == '確認FB':
                requests.post(os.getenv("DISCORD_WEBHOOK"), message.fb_message(task_result))


db_handler = TaskDBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB()
message = Message(db_handler, user_db, os.getenv("CONFIRM_USER"))

WatchTaskStatus()
