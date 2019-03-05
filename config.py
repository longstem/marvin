import logging
import os
from logging import StreamHandler

from pythonjsonlogger import jsonlogger


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '-')
    SSL_REDIRECT = False
    SERVER_NAME = os.environ.get('SERVER_NAME')

    DEFAULT_SUBDOMAIN = os.environ.get('DEFAULT_SUBDOMAIN')
    API_URL_PREFIX = os.environ.get('API_URL_PREFIX', '/api')

    API_SUBDOMAIN = os.environ.get('API_SUBDOMAIN', DEFAULT_SUBDOMAIN)

    SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
    SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', '')

    SLACK_EVENT_CONTEXT = {
        'bot_id': os.environ.get('SLACK_BOT_ID'),
        'bot_user_id': os.environ.get('SLACK_BOT_USER_ID'),
    }

    @staticmethod
    def init_app(app):
        """Init app"""


class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app(app):
        log_handler = StreamHandler()
        formatter = jsonlogger.JsonFormatter(json_indent=4)
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(formatter)

        app.logger.handlers[:] = []
        app.logger.addHandler(log_handler)


class TestConfig(DevelopmentConfig):
    TESTING = True


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        from raven.contrib.flask import Sentry
        sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
        sentry.init_app(app)


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
