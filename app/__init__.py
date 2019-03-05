import asyncio
import os

from flask import Flask

import flask_login
import flask_slack
from flask_slack.signals import event_received
from flask_sslify import SSLify
from slackclient import SlackClient

from config import config

login_manager = flask_login.LoginManager()
slack_manager = flask_slack.SlackManager()

from . import handlers  # NOQA: F401 isort:skip

__all__ = [
    'create_app',
    'handlers',
    'login_manager',
    'slack_manager',
]


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api import api as api_blueprint  # isort:skip
    from .main import main as main_blueprint  # isort:skip

    login_manager.init_app(app)
    slack_manager.init_app(app, blueprint=api_blueprint)

    app.api_call = SlackClient(app.config['SLACK_API_TOKEN']).api_call

    @event_received.connect_via(app)
    def event_logger(sender, data, **extra):
        app.logger.debug(data['event'])

    @slack_manager.context_processor
    def context_processor(data):
        return app.config['SLACK_EVENT_CONTEXT']

    @slack_manager.dispatch_event_handler
    def async_event_dispatcher(sender, data, handlers, **extra):
        coroutines = [h(sender, data, **extra) for h in handlers]
        asyncio.run(asyncio.wait(coroutines))

    if app.config['SSL_REDIRECT']:
        SSLify(app)

    app.register_blueprint(
        main_blueprint,
        subdomain=app.config['DEFAULT_SUBDOMAIN'])

    app.register_blueprint(
        api_blueprint,
        url_prefix=os.path.join(app.config['API_URL_PREFIX'], 'v1'),
        subdomain=app.config['API_SUBDOMAIN'])

    return app
