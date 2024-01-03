import os
import jokekappa
import requests
import xml.etree.ElementTree as ET

from flask import Flask
from flask_apscheduler import APScheduler

from helper.linebot_init import line_bot

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

class Config:
    SCHEDULER_API_ENABLED = True

def daily_job(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('cron', id='weekday_joke', day_of_week='mon-fri', hour=9, minute=30)
    def weekday_joke():
        group_id = os.getenv('GROUP_ID')

        joke = jokekappa.get_joke()
        text_content = '各位社畜早安，早餐吃了嗎？還有多少 issues 沒解？今天會不會又噴什麼垃圾 bug？為你們送上今天的笑話以及 iThome 前十二篇文章，祝你們今天偷薪水愉快。\n\n' + joke

        line_bot_api.push_message(group_id, TextSendMessage(text=text_content))

    @scheduler.task('cron', id='weekend_joke', day_of_week='sat-sun', hour=11, minute=30)
    def weekend_joke():
        group_id = os.getenv('GROUP_ID')

        joke = jokekappa.get_joke()
        text_content = '各位放假仔早安，為你們送上今天的笑話以及 iThome 前十二篇文章，祝你們今天放假愉快。\n\n' + joke

        line_bot_api.push_message(group_id, TextSendMessage(text=text_content))

    @scheduler.task('cron', id='weekday_joke', day_of_week='mon-fri', hour=9, minute=31)
    def weekday_ithome():
        group_id = os.getenv('GROUP_ID')

        url = "https://www.ithome.com.tw/rss"
        response = requests.get(url)
        xml_data = response.text

        root = ET.fromstring(xml_data)

        news_list = []
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            news_list.append({'title': title, 'link': link})

        flex_dict = {
            "type": "carousel",
            "contents": []
        }

        selected_news_list = news_list[:12]
        for news in selected_news_list:
            bubble_dict = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": news['title'],
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "Go",
                                "uri": news['link']
                            }
                        }
                    ]
                }
            }
            flex_dict['contents'].append(bubble_dict)

        flex_message = FlexSendMessage(
            alt_text='ithome',
            contents=flex_dict
        )

        line_bot_api.push_message(group_id, flex_message)

    @scheduler.task('cron', id='weekend_joke', day_of_week='sat-sun', hour=11, minute=31)
    def weekend_ithome():
        group_id = os.getenv('GROUP_ID')

        url = "https://www.ithome.com.tw/rss"
        response = requests.get(url)
        xml_data = response.text

        root = ET.fromstring(xml_data)

        news_list = []
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            news_list.append({'title': title, 'link': link})

        flex_dict = {
            "type": "carousel",
            "contents": []
        }

        selected_news_list = news_list[:12]
        for news in selected_news_list:
            bubble_dict = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": news['title'],
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "Go",
                                "uri": news['link']
                            }
                        }
                    ]
                }
            }
            flex_dict['contents'].append(bubble_dict)

        flex_message = FlexSendMessage(
            alt_text='ithome',
            contents=flex_dict
        )

        line_bot_api.push_message(group_id, flex_message)

    scheduler.start()

    