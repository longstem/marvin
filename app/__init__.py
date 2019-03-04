import asyncio
import os

from flask import Flask, current_app

import flask_login
import flask_slack
from flask_slack.signals import event_received
from flask_sslify import SSLify
from slackclient import SlackClient

from config import config

from .api import api as api_blueprint
from .main import main as main_blueprint

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

    login_manager.init_app(app)
    slack_manager.init_app(app, blueprint=api_blueprint)

    @event_received.connect_via(app)
    def slack_client(sender, data, **extra):
        slack_api_token = sender.config['SLACK_API_TOKEN']
        sender.api_call = SlackClient(slack_api_token).api_call

    @slack_manager.context_processor
    def context_processor(data):
        return current_app.config['SLACK_EVENT_CONTEXT']

    @slack_manager.dispatch_event_handler
    def async_event_dispatcher(sender, data, handlers, **extra):
        coroutines = [h(sender, data, **extra) for h in handlers]

        # Python 3.6
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(coroutines))
        loop.close()

        # Python 3.7 (zappa does not support it)
        # asyncio.run(asyncio.wait(coroutines))

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
