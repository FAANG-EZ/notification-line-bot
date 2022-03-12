import os
import sys

from github_webhook import Webhook

from flask import Flask, request, abort
from api.controller.callback import callback_controller
from api.controller.postreceive import postreceive_controller


app = Flask(__name__)
webhook = Webhook(app, secret='mTPwE4-tcT-XN2X') # Defines '/postreceive' endpoint

@app.route("/callback", methods=['POST'])
def callback():
    result = callback_controller()

    return "Ok!"

# @webhook.hook(event_type='ping')
@webhook.hook(event_type='push')
def on_push(data):
    result = postreceive_controller(data)