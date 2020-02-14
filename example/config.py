import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisneedstobechanged'
    FLASK_TOTP_SECRET = os.environ.get('FLASK_TOTP_SECRET') or 'andthistoo'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/apple' or \
        'sqlite:///' + os.path.join(basedir, 'apple.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_AS_ASCII = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
