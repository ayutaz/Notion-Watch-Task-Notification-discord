import os

from dotenv import load_dotenv

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB

load_dotenv()


def WatchTaskStatus():
    db = db_handler.get_change_history(5)
    for task_result in db:
        if task_result is not None:
            if db_handler.task_status(task_result) == '確認依頼:':
                print(message.confirm_message("test"))
            elif db_handler.task_status(task_result) == '対応中':
                print(message.fb_message("test"))


db_handler = TaskDBHandler(os.getenv("NOTION_TOKEN"))
user_db = UserDB()
message = Message(db_handler, user_db, os.getenv("CONFIRM_USER"))

WatchTaskStatus()
