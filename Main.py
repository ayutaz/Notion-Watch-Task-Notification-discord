import os
from pprint import pprint

from notion_client import Client

from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

db = notion.databases.query(
    **{
        'database_id': os.getenv("PRIVATE_DB"),
        "filter": {
            "property": "Deadline",
            "select": {
                "equals": 'Done'
            }
        }
    }
)
results = db['results']
for idx in range(len(results)):
    is_done = results[idx]['properties']['Deadline']['select']
    if is_done is None:
        continue
    page_id = results[idx]['id']
    if is_done != 'Done':
        print(is_done['name'] + ': ' + page_id)
        print('\n')
