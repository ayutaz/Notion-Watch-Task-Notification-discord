import os

from dotenv import load_dotenv

from DBHandler import DBHandler

load_dotenv()


def TaskWatch(db_id):
    results = db_handler.get_done_task_db(db_id)
    for idx in range(len(results)):
        done_date = db_handler.get_done_date(results[idx])
        print(db_handler.get_task_name(results[idx]))
        print(done_date)
        page_id = db_handler.get_page_id(results[idx])
        print(page_id)
        print('\n')
        db_handler.update_task_date(page_id)


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))

TaskWatch(os.getenv("PRIVATE_DB"))
