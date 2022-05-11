import json


class UserDB:
    def __init__(self, users):
        self.users = self.add_users(users)

    @staticmethod
    def add_users(users):
        users = json.loads(users)
        return users

    def get_user_id(self, name):
        try:
            return self.users[name]
        except KeyError:
            print('no user found')
            return None
