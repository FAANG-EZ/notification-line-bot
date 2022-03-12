import os
import sys

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

class line_bot:
    def __init__(self):
        channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        channel_secret = os.getenv('LINE_CHANNEL_SECRET')
        if not channel_access_token:
            print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
            sys.exit(1)
        if not channel_secret:
            print('Specify LINE_CHANNEL_SECRET as environment variable.')
            sys.exit(1)

        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)