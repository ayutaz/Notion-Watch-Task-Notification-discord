import datetime

from notion_client import Client


class TaskDBHandler:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.date.today()

    def get_change_history(self) -> list:
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
        task_list = []
        for result in db['results']:
            if result['properties']['ステータス']['select'] is not None:
                task_list.append(result)
        return task_list

    def get_deadline_task(self, db_id: str, deadline: str):
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
    def get_task_name(db_result) -> str:
        return db_result['properties']['Name']['title'][0]['plain_text']

    @staticmethod
    def get_task_deadline(db_result) -> dict:
        if db_result['properties']['期日']['date'] is not None:
            return db_result['properties']['期日']['date']['start']
        else:
            return None

    @staticmethod
    def task_status(db_result) -> dict:
        return db_result['properties']['ステータス']['select']['name']

    def is_task_status_doing_from_confirm(self, result) -> bool:
        status = result['properties']['ステータス']['select']['name']
        pre_status = result['properties']['preStatus']['select']['name']
        if status == '対応中' and pre_status == '確認依頼':
            self.update_task_preStatus(result['id'], status)
            return True
        else:
            return False

    def is_task_status_confirm_from_doing(self, result) -> bool:
        status = result['properties']['ステータス']['select']['name']
        if status == '確認依頼':
            self.update_task_preStatus(result['id'], status)
            return True
        else:
            return False

    def update_task_preStatus(self, page_id: str, status: str) -> None:
        self.notion.pages.update(
            page_id,
            properties={
                'preStatus':
                    {
                        'select':
                            {
                                'name': status
                            }
                    }
            }
        )

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

    @staticmethod
    def get_last_edited_time(db_result):
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
