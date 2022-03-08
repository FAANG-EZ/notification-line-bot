import os
import sys

from flask import Flask, request, abort
from api.controller.callback import callback_controller

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    result = callback_controller()

    return "Ok!"
