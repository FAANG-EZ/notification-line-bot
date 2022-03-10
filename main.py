from flask import Flask
from api.route.linebot import app

from cron.daily_joke import daily_joke

if __name__ == "__main__":
    daily_joke(app)
    app.run(host='0.0.0.0', port=80)