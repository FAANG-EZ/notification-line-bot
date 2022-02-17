from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('taDZDTE2Bniahyj04tr5txxVE4OXEkNXRkQi6Y0cFLRqFFeEktn03w3AfuL/kTf6IclaOH0eclxMsBp0oiIQr2FsQbbg+vCq0ksRKm9Bu4M57HkIIHSarVemRIYSbct4tcIVazxAxulyKYbLqxqOcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f8ae45e1e020dba71be6addad24fb3c1')

@app.route("/callback", methods=['POST'])
def callback():
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

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="我不是一台機器人")
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)