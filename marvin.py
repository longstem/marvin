import os

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG', 'default'))


@app.cli.command()
def profile():
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
    app.run()


@app.cli.command()
def deploy():
    """Run deployment tasks"""
