import os
import sys

import jokekappa

from flask import Flask
from flask_apscheduler import APScheduler

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
if not channel_access_token:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if not channel_secret:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

class Config:
    SCHEDULER_API_ENABLED = True

def daily_joke(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('cron', id='write_log', hour=9, minute=30)
    def write_log():
        group_id = os.getenv('GROUP_ID')
        line_bot_api.push_message(group_id, TextSendMessage(text='各位社畜早安，早餐吃了嗎？還有多少 issues 沒解？今天會不會又噴什麼垃圾 bug？為你們送上今天的笑話，祝你們今天上班愉快。'))
        joke = jokekappa.get_joke()
        line_bot_api.push_message(group_id, TextSendMessage(text=joke['content']))

    scheduler.start()

    