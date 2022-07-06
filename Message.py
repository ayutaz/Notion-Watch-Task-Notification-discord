class Message:
    def __init__(self, db_handler, user_db, pdm_name):
        self.db_handler = db_handler
        self.user_db = user_db
        self.PdM_name = pdm_name

    def deadLineMessage(self, result):
        manager_users = self.db_handler.get_task_manager_name(result)
        review_users = self.db_handler.get_task_reviewer_name(result)
        task_url = self.db_handler.get_task_url(result)
        content = {
            "username": "期日が迫っているタスク通知bot",
            "content": f"{self.mention_users_message(manager_users)} cc {self.mention_users_message(review_users)} "
                       f"\nタスク名: {self.db_handler.get_task_name(result)}"
                       f"\n期日：{self.db_handler.get_task_deadline(result)}"
                       f"\nタスクの残り期日が3日以内です。"
                       f"\n作業の進捗を確認して、期日以内の完了が難しければ{self.PdM_name}に相談してください。"
                       f"\nタスクURL:{task_url}"
        }
        return content

    def confirm_message(self, result):
        manager_users = self.db_handler.get_task_manager_name(result)
        review_users = self.db_handler.get_task_reviewer_name(result)
        task_url = self.db_handler.get_task_url(result)
        content = {
            "username": "タスク確認依頼bot",
            "content": f"{self.mention_users_message(review_users)} cc {self.mention_users_message(manager_users)} "
                       f"\nタスク名: {self.db_handler.get_task_name(result)}"
                       f"\n期日：{self.db_handler.get_task_deadline(result)}"
                       f"\nあなた宛てに確認依頼タスクが更新されました。"
                       f"\n確認をお願いします。"
                       f"\nタスクURL:{task_url}"
        }
        print(content)
        return content

    def fb_message(self, result):
        manager_users = self.db_handler.get_task_manager_name(result)
        review_users = self.db_handler.get_task_reviewer_name(result)
        content = {
            "username": "タスク確認FBbot",
            "content": f"{self.mention_users_message(manager_users)} cc {self.mention_users_message(review_users)} "
                       f"\nタスク名: {self.db_handler.get_task_name(result)}"
                       f"\n期日：{self.db_handler.get_task_deadline(result)}"
                       f"\nあなた宛てに確認FBでタスクが更新されました。"
                       f"\n確認、対応をお願いします。"
        }
        return content

    def mention_users_message(self, user_result):
        mention_content = ""
        for user in user_result:
            mention_content += self.mention_user_message(self.user_db.get_user_id(user))
        return mention_content

    @staticmethod
    def mention_user_message(user_id):
        return f"<@{user_id}>"
