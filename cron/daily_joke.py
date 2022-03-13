import os
import jokekappa

from flask import Flask
from flask_apscheduler import APScheduler

from helper.linebot_init import line_bot

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

class Config:
    SCHEDULER_API_ENABLED = True

def daily_joke(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('cron', id='weekday_joke', day_of_week='mon-fri', hour=9, minute=30)
    def weekday_joke():
        group_id = os.getenv('GROUP_ID')
        line_bot_api.push_message(group_id, TextSendMessage(text='各位社畜早安，早餐吃了嗎？還有多少 issues 沒解？今天會不會又噴什麼垃圾 bug？為你們送上今天的笑話，祝你們今天上班愉快。'))
        joke = jokekappa.get_joke()
        line_bot_api.push_message(group_id, TextSendMessage(text=joke['content']))

    @scheduler.task('cron', id='weekend_joke', day_of_week='sat-sun', hour=11, minute=30)
    def weekend_joke():
        group_id = os.getenv('GROUP_ID')
        line_bot_api.push_message(group_id, TextSendMessage(text='各位放假仔早安，為你們送上今天的笑話，祝你們今天放假愉快。'))
        joke = jokekappa.get_joke()
        line_bot_api.push_message(group_id, TextSendMessage(text=joke['content']))

    scheduler.start()

    