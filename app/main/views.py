from flask import abort, current_app, render_template, request

from . import main


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)

    shutdown = request.environ.get('werkzeug.server.shutdown')

    if not shutdown:
        abort(500)

    shutdown()
    return 'Shutting down...'


@main.route('/')
def dont_panic():
    return render_template('main/dont_panic.html')
