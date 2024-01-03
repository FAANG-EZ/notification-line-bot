from flask import Flask
from api.route.linebot import app

from cron.daily_job import daily_job

if __name__ == "__main__":
    daily_job(app)
    app.run(host='0.0.0.0', port=80)