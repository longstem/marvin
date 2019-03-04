import logging
import os
from logging import StreamHandler


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '-')
    SSL_REDIRECT = False
    SERVER_NAME = os.environ.get('SERVER_NAME')

    DEFAULT_SUBDOMAIN = os.environ.get('DEFAULT_SUBDOMAIN')
    API_URL_PREFIX = os.environ.get('API_URL_PREFIX', '/api')
    API_SUBDOMAIN = os.environ.get('API_SUBDOMAIN')

    SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
    SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', '')

    @staticmethod
    def init_app(app):
        """Init app"""


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        from raven.contrib.flask import Sentry
        sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
        sentry.init_app(app)


class DockerConfig(DevelopmentConfig):

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig,
}
