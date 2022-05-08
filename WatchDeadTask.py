import os

import requests
from dotenv import load_dotenv

from DBHandler import DBHandler

load_dotenv()


def WatchDeadTask(db_id):
    results = db_handler.get_deadline_task(db_id, 3)
    for idx in range(len(results)):
        print(db_handler.get_task_name(results[idx]))
        content = {
            "username": "期日が迫っているタスク通知bot",
            "content": f"「{db_handler.get_task_name(results[idx])}」が期日迫っています。"
        }
        requests.post(os.getenv("DISCORD_WEBHOOK"), content)


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))

WatchDeadTask(os.getenv("DB"))
