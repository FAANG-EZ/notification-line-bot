import re

from flask import Flask, abort, request
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from helper.joke import Joke
from helper.linebot_init import line_bot
from logger.logger import logger

app = Flask(__name__)

line_bot = line_bot()
line_bot_api = line_bot.line_bot_api
handler = line_bot.handler

joke = Joke()

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
            logger.error("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('^說個笑話$',message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=joke.generate_joke())
        )