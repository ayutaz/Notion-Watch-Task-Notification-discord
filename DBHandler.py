import datetime
import string

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.date.today()

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

    @staticmethod
    def get_task_manager_name(db_result):
        req_manager_list = db_result['properties']['担当者']['people']
        manager_list = []
        for manager in req_manager_list:
            manager_list.append(manager['name'])

        return manager_list

    @staticmethod
    def get_task_reviewer_name(db_result):
        req_reviewer_list = db_result['properties']['確認者']['people']
        reviewer_list = []
        for reviewer in req_reviewer_list:
            reviewer_list.append(reviewer['name'])

        return reviewer_list
