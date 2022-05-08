import datetime
import string

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.date.today()

    def get_deadline_task(self, db_id: string, deadline: int):
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
                                "on_or_before": (self.today + datetime.timedelta(days=deadline)).isoformat(),
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
