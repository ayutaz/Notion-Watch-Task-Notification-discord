import os

from dotenv import load_dotenv

from DBHandler import DBHandler

load_dotenv()


def WatchDeadTask(db_id):
    results = db_handler.get_deadline_task(db_id, 3)
    for idx in range(len(results)):
        print(db_handler.get_task_name(results[idx]))


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))

WatchDeadTask(os.getenv("DB"))
