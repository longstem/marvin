from functools import wraps

from flask import abort

from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_view
    return decorator
