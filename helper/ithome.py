import xml.etree.ElementTree as ET

import requests
from linebot.models import FlexSendMessage

from logger.logger import logger


class Ithome:
    def __init__(self):
        pass

    def get_ithome_rss(self, num_news=12):
        try:
            url = "https://www.ithome.com.tw/rss"
            response = requests.get(url)
            xml_data = response.text

            root = ET.fromstring(xml_data)

            news_list = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                link = item.find('link').text
                news_list.append({'title': title, 'link': link})

            return news_list[:num_news]
        except Exception as e:
            error_message = "An unexpected error occurred on get ithome rss: " + str(e)
            logger.error(error_message)
    
    def create_flex_message(self, news_list):
        try:
            flex_dict = {
                "type": "carousel",
                "contents": []
            }

            for news in news_list:
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

            return flex_message
        except Exception as e:
            error_message = "An unexpected error occurred on create ithome flex message: " + str(e)
            logger.error(error_message)