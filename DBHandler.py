import datetime

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)

    def get_done_task_db(self, db_id):
        db = self.notion.databases.query(
            **{
                'database_id': db_id,
                "filter": {
                    "and": [
                        {
                            "property": "期限",
                            "select": {
                                "equals": 'Done'
                            }
                        },
                        {
                            "property": "日付",
                            "date": {
                                "is_empty": True
                            }
                        }

                    ]
                }
            }
        )
        return db['results']

    def update_task_date(self, page_id):
        today = str(datetime.datetime.now().isoformat())
        self.notion.pages.update(
            page_id,
            properties={
                '日付': {
                    'date': {
                        'start': today,
                        'time_zone': 'Asia/Tokyo'
                    }
                }
            }
        )

    @staticmethod
    def get_done_date(db_result):
        return db_result['properties']['日付']['date']

    @staticmethod
    def get_task_name(db_result):
        return db_result['properties']['タスク名']['title'][0]['plain_text']

    @staticmethod
    def get_page_id(db_result):
        return db_result['id']
