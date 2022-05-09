import os
import json


class UserDB:
    def __init__(self):
        self.users = self.add_users()

    def add_users(self):
        users = json.loads(os.getenv("USERS"))
        print(users)
        return users

    def get_user_id(self, name):
        try:
            return self.users[name]
        except KeyError:
            print('no user found')
            return None
