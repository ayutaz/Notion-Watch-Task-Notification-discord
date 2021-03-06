# Notion-Watch-Task-Notification-discord

以下のタスクを監視して、discordで通知を行うbot

ベースのソースコードは [Notion-Task-Watch](https://github.com/ayutaz/Notion-Task-Watch)です。

# what can it do?

- [x] Notionで完了以外のいずれかのステータスで期限まであと3日まで迫っているタスクをdiscordで全体通知

discordでの通知メッセージは以下のようになります。

```
@ようさん cc @ようさん 
タスク名: テスト
期日：2022-05-11
タスクの残り期日が3日以内です。
作業の進捗を確認して、期日以内の完了が難しければ ようさんに相談してください。
タスクURL:https://www.notion.so/page_url
```

- [x] Notionでタスクのステータスが確認待ちから対応中に変更された際に担当者へ、確認依頼に変更された際に確認者へdiscordにタスク名を通知

discordでの通知メッセージは以下のようになります。

```
@ようさんcc @ようさん
タスク名: ステータス変更テスト1
期日：2022-05-10
あなた宛てに確認依頼タスクが更新されました。
確認をお願いします。
タスクURL:https://www.notion.so/page_url
```

```
@ようさんcc @ようさん
タスク名: ステータス変更テスト1
期日：2022-05-10
あなた宛てに確認FBでタスクが更新されました。
確認、対応をお願いします。
タスクURL:https://www.notion.so/page_url
```

実装に関する記事

* [Notionのタスク 一覧でタスクがDoneになったときに完了日付を自動入力する【Notion,Python,GitHub Actions】](https://ayousanz.hatenadiary.jp/entry/Notion%E3%81%AE%E3%82%BF%E3%82%B9%E3%82%AF_%E4%B8%80%E8%A6%A7%E3%81%A7%E3%82%BF%E3%82%B9%E3%82%AF%E3%81%8CDone%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%9F%E3%81%A8%E3%81%8D%E3%81%AB%E5%AE%8C%E4%BA%86%E6%97%A5%E4%BB%98)
* [Notionのタスクのステータス変更をDiscordでメッセージを送る【Discord.py,Notion API,GitHub Actions,cron-job】]()

# requirements

* Python 3.9
* [notion-client](https://github.com/ramnes/notion-sdk-py) :for python notion api wrapper

# setup

1. fork this repository

## Notion set up

2. get notion api
3. get notion db url

## discord set up

4. get discord webhook url

## gitHub set up

5. create db for notion name - discord id.
   Create a DB with the following dictionary type, in which the Notion display name and the discordID are linked.

```
USERS={"userName":"discord User ID"}
```

6. set gitHub action secret for values

Finally, the environment variables are set as follows.

```
NOTION_TOKEN='notion token'
DB='notion db id'
DISCORD_WEBHOOK='discord webhook url'
DEADLINE_LIMIT_DAYS= deadline limit days(int)
USERS={"userName":"discord User ID"}
CONFIRM_USER='user name'
```

7. About Periodic Execution

If you want strictly periodic execution, use other periodic execution services.
GitHub Actions only adds tasks to the Queue and does not guarantee execution. [Details](https://upptime.js.org/blog/2021/01/22/github-actions-schedule-not-working/)
I use [cron-job](https://cron-job.org/en/) for strictly scheduled execution (every minute).

For other information, Notion's DB must be set up as shown in the following image. However, not all information is required.
To run this program, all you need is the `person in charge`, `confirmation person`, `due date`, and `preStatus`.
(I use `preStatus` as a pseudo variable for internal processing)

![](docs/NotionDB.png)

# Architecture diagram

```mermaid
sequenceDiagram
    participant cronJob as cron env
    participant Task Function as GitHub Actions dispatch
    participant message as Discord WebHook

    cronJob ->>+ Task Function: workflowの実行
    Task Function ->>+ message: discordへのメッセージ送信
    message -->>- Task Function: 200
    Task Function -->>- cronJob: 200
```
