from . import api


@api.route('/ping')
def ping():
    return '', 204
