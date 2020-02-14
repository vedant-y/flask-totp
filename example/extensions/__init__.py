from flask_sqlalchemy import SQLAlchemy

from .flask_totp import FlaskTOTP

db = SQLAlchemy()
totp = FlaskTOTP()
