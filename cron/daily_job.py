import os

from flask_apscheduler import APScheduler
from linebot.models import TextSendMessage

from helper.ithome import Ithome
from helper.joke import Joke
from helper.linebot_init import line_bot
from logger.logger import logger

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

joke = Joke()
ithome = Ithome()

class Config:
    SCHEDULER_API_ENABLED = True

def daily_job(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('cron', id='weekday', day_of_week='mon-fri', hour=9, minute=30)
    def weekday():
        group_id = os.getenv('GROUP_ID')

        # Joke
        try:
            text_content = '各位社畜早安，早餐吃了嗎？還有多少 issues 沒解？今天會不會又噴什麼垃圾 bug？為你們送上今天的笑話以及 iThome 前十二篇文章，祝你們今天偷薪水愉快。\n\n'
            line_bot_api.push_message(group_id, TextSendMessage(text=joke.generate_joke(custom_message=text_content)))
        except Exception as e:
            error_message = "An unexpected error occurred on weekday joke: " + str(e)
            logger.error(error_message)

        # iThome
        try:
            news_list = ithome.get_ithome_rss(num_news=12)
            flex_message = ithome.create_flex_message(news_list=news_list)
            line_bot_api.push_message(group_id, flex_message)
        except Exception as e:
            error_message = "An unexpected error occurred on weekday iThome: " + str(e)
            logger.error(error_message)

    @scheduler.task('cron', id='weekend', day_of_week='sat-sun', hour=11, minute=30)
    def weekend():
        group_id = os.getenv('GROUP_ID')

        # Joke
        try:
            text_content = '各位放假仔早安，為你們送上今天的笑話以及 iThome 前十二篇文章，祝你們今天放假愉快。\n\n'
            line_bot_api.push_message(group_id, TextSendMessage(text=joke.generate_joke(custom_message=text_content)))
        except Exception as e:
            error_message = "An unexpected error occurred on weekend joke: " + str(e)
            logger.error(error_message)

        # iThome
        try:
            news_list = ithome.get_ithome_rss(num_news=12)
            flex_message = ithome.create_flex_message(news_list=news_list)
            line_bot_api.push_message(group_id, flex_message)

        except Exception as e:
            error_message = "An unexpected error occurred on weekend iThome: " + str(e)
            logger.error(error_message)
    scheduler.start()
