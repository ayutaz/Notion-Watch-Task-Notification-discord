import contextlib
import datetime
import io
import unittest
from unittest import mock

from Message import Message
from TaskDBHandler import TaskDBHandler
from UserDB import UserDB


def make_task(status=None, pre_status=None, title=("テスト",), managers=("ようさん",), reviewers=("ようさん",)):
    return {
        "id": "page-id",
        "url": "https://www.notion.so/page_url",
        "properties": {
            "Name": {"title": [{"plain_text": text} for text in title]},
            "ステータス": {"select": None if status is None else {"name": status}},
            "preStatus": {"select": None if pre_status is None else {"name": pre_status}},
            "期日": {"date": {"start": "2022-05-11"}},
            "担当者": {"people": [{"name": name} for name in managers]},
            "確認者": {"people": [{"name": name} for name in reviewers]},
        },
    }


class TaskDBHandlerTests(unittest.TestCase):
    def setUp(self):
        self.handler = TaskDBHandler("dummy-token")
        self.handler.notion = mock.MagicMock()
        self.handler.today = datetime.date(2022, 5, 8)

    def test_status_change_detection_ignores_pages_without_task_properties(self):
        self.assertTrue(TaskDBHandler.is_change_task_status(make_task("確認依頼", "対応中")))
        self.assertFalse(TaskDBHandler.is_change_task_status(make_task("対応中", "対応中")))
        self.assertFalse(TaskDBHandler.is_change_task_status(make_task(None, "対応中")))
        self.assertFalse(TaskDBHandler.is_change_task_status({"properties": {"title": {}}}))

    def test_task_name_joins_all_title_segments(self):
        self.assertEqual(TaskDBHandler.get_task_name(make_task(title=("資料", "作成"))), "資料作成")
        self.assertEqual(TaskDBHandler.get_task_name(make_task(title=())), "")

    def test_deadline_query_uses_limit_days_and_follows_pagination(self):
        self.handler.notion.databases.query.side_effect = [
            {"results": [{"id": "1"}], "has_more": True, "next_cursor": "cursor-1"},
            {"results": [{"id": "2"}], "has_more": False, "next_cursor": None},
        ]

        results = self.handler.get_deadline_task("db-id", "3")

        self.assertEqual([result["id"] for result in results], ["1", "2"])
        first, second = self.handler.notion.databases.query.call_args_list
        date_filter = first.kwargs["filter"]["and"][1]["date"]
        self.assertEqual(date_filter, {"on_or_before": "2022-05-11", "on_or_after": "2022-05-08"})
        self.assertEqual(first.kwargs["database_id"], "db-id")
        self.assertNotIn("start_cursor", first.kwargs)
        self.assertEqual(second.kwargs["start_cursor"], "cursor-1")


class MessageTests(unittest.TestCase):
    def setUp(self):
        self.user_db = UserDB('{"ようさん": "1234"}')

    def test_deadline_message_mentions_users_and_uses_configured_days(self):
        message = Message(TaskDBHandler, self.user_db, "ようさん", "5")

        content = message.deadLineMessage(make_task("対応中", "対応中"))["content"]

        self.assertTrue(content.startswith("<@1234> cc <@1234> "))
        self.assertIn("期日：2022-05-11", content)
        self.assertIn("タスクの残り期日が5日以内です。", content)
        self.assertIn("タスクURL:https://www.notion.so/page_url", content)

    def test_unknown_user_is_not_rendered_as_none_mention(self):
        message = Message(TaskDBHandler, self.user_db, "ようさん")

        with contextlib.redirect_stdout(io.StringIO()):
            content = message.fb_message(make_task(managers=("未登録",)))["content"]

        self.assertNotIn("<@None>", content)
        self.assertTrue(content.startswith("@未登録 cc <@1234> "))

    def test_confirm_message_does_not_print_task_details(self):
        message = Message(TaskDBHandler, self.user_db, "ようさん")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            content = message.confirm_message(make_task("確認依頼", "対応中"))

        self.assertEqual(output.getvalue(), "")
        self.assertEqual(content["username"], "タスク確認依頼bot")


if __name__ == "__main__":
    unittest.main()
