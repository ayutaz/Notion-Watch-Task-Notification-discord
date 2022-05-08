import os
import json


class UserDB:
    def __init__(self):
        self.users = self.add_users()

    def add_users(self):
        users = json.loads(os.getenv("USERS"))
        return users

    def get_user_id(self, name):
        return self.users[name]
