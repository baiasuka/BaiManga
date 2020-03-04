from flask import Flask, render_template
from flask_cors import CORS
from flask_apscheduler import APScheduler

from schedule_tasks import schedule_config
from models import db
import config
from resource import create_api


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_object(schedule_config)
    scheduler = APScheduler()
    api = create_api()
    api.init_app(app)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # 解决跨域问题
    CORS(app)
    return app

