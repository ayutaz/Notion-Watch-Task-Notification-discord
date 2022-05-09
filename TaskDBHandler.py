import datetime
import string

from notion_client import Client


class TaskDBHandler:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.date.today()

    def get_change_history(self, get_history_minutes: int):
        now = datetime.datetime.now().astimezone(datetime.timezone.utc)
        db = self.notion.search(
            **{
                "sort": {
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                },
                "filter": {
                    "value": "page",
                    "property": "object"
                },
                "page_size": 100,
            }
        )
        history_list = []
        for history in db['results']:
            last_edited_time = datetime.datetime.fromisoformat(history['last_edited_time'].replace('Z', '+00:00'))
            dt = now - datetime.timedelta(minutes=get_history_minutes)
            if dt < last_edited_time:
                history_list.append(history)
        return history_list

    def get_deadline_task(self, db_id: string, deadline: string):
        db = self.notion.databases.query(
            **{
                'database_id': db_id,
                "filter": {
                    "and": [
                        {
                            "property": "ステータス",
                            "select": {
                                "does_not_equal": '完了'
                            }
                        },
                        {
                            "property": "期日",
                            "date": {
                                "on_or_before": (self.today + datetime.timedelta(days=int(deadline))).isoformat(),
                                "on_or_after": self.today.isoformat()
                            }
                        }

                    ]
                }
            }
        )
        return db['results']

    @staticmethod
    def get_task_name(db_result):
        return db_result['properties']['Name']['title'][0]['plain_text']

    @staticmethod
    def get_task_deadline(db_result):
        return db_result['properties']['期日']['date']['start']

    def task_status(self, db_result):
        return db_result['properties']['ステータス']['select']['name']

    @staticmethod
    def get_task_manager_name(db_result):
        req_manager_list = db_result['properties']['担当者']['people']
        manager_list = []
        for manager in req_manager_list:
            try:
                manager_list.append(manager['name'])
            except KeyError:
                print('no name in manager')

        return manager_list

    def get_last_edited_time(self, db_result):
        return db_result['last_edited_time']

    @staticmethod
    def get_task_reviewer_name(db_result):
        req_reviewer_list = db_result['properties']['確認者']['people']
        reviewer_list = []
        for reviewer in req_reviewer_list:
            try:
                reviewer_list.append(reviewer['name'])
            except KeyError:
                print('no name in reviewer')

        return reviewer_list
