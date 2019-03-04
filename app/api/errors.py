from flask import jsonify

from ..exceptions import ValidationError
from . import api


def bad_request(message):
    return jsonify({'error': 'bad request', 'message': message}), 400


def unauthorized(message):
    return jsonify({'error': 'unauthorized', 'message': message}), 401


def forbidden(message):
    return jsonify({'error': 'forbidden', 'message': message}), 403


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
