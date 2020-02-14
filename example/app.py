from flask import Flask
import os

from config import DevelopmentConfig
from extensions import db
from extensions import totp
from main import main

def create_app():
    app = _setup_app()
    _setup_blueprint(app)
    _setup_config(app)
    _setup_database(app)
    _setup_totp(app)
    return app

def _setup_app():
    app = Flask(__name__)
    return app

def _setup_blueprint(app):
    app.register_blueprint(main)

def _setup_config(app):
    app.config.from_object(os.environ.get('APP_CONFIG') or DevelopmentConfig)

def _setup_database(app):
    db.init_app(app)

def _setup_totp(app):
    totp.init_app(app)

if __name__ == '__main__':
    app = create_app()
    app.run()
