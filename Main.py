import os
from pprint import pprint

from notion_client import Client

from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

db = notion.databases.query(
    **{
        'database_id': os.getenv("PRIVATE_DB")  # データベースID
    }
)
results = db['results']
for idx in range(len(results)):
    is_done = results[idx]['properties']['Deadline']['select']
    if is_done is None:
        continue
    print(is_done['name'])
    print('\n')
