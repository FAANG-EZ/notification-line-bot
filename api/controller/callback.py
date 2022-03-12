import jokekappa

import re

from flask import Flask, request, abort

from helper.linebot_init import line_bot

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

class callback_controller:
    def __init__(self):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('^說個笑話聽聽$',message):
        joke = jokekappa.get_joke()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=joke['content'])
        )