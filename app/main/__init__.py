from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from . import errors, views  # NOQA E402 isort:skip

__all__ = ['main', 'errors', 'views']
