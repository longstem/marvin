from flask import Blueprint

api = Blueprint('api', __name__)

from . import errors, views  # NOQA E402 isort:skip

__all__ = ['api', 'errors', 'views']
