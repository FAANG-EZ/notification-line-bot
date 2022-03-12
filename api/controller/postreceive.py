from flask import Flask, request, abort

from helper.linebot_init import line_bot

from linebot.models import (
    FlexSendMessage
)

app = Flask(__name__)

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

class postreceive_controller:
    def __init__(self, data):

        sender_uri = data.get('sender', {}).get('html_url')
        sender_avatar_url = data.get('sender', {}).get('avatar_url')
        sender_name = data.get('sender', {}).get('login')

        repo_name = data.get('repository', {}).get('name')
        commits_count = str(len(data.get('commits')))
        commits_compare = data.get('compare')

        contents_box = [
            {
                "type": "text",
                "weight": "bold",
                "size": "xl",
                "text": sender_name,
                "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": sender_uri
                }
            },
            {
                "type": "box",
                "layout": "baseline",
                "margin": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "[" + repo_name + "] " + commits_count + " new commit",
                    "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": commits_compare
                    },
                    "color": "#0366d6"
                }
                ],
                "borderWidth": "none"
            },
        ]
        for idx, commit in enumerate(data.get('commits')):
            contents_box.append(
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "[" + commit.get('id')[0:7] + "] - " + commit.get('message'),
                                "size": "sm",
                                "color": "#ffffff",
                                "margin": "sm",
                                "wrap": True
                            }
                            ],
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": commit.get('url')
                            },
                            "backgroundColor": "#3c3c3c"
                        }
                    ]
                }
            )

        flex_message = FlexSendMessage(
            alt_text='Hi, here is a push notification!',
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": commits_compare
                    },
                    "url": sender_avatar_url
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents_box
                }
            }
        )

        group_id = os.getenv('GROUP_ID')
        line_bot_api.push_message(group_id, flex_message)


