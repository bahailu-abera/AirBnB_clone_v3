"""
Application logic
"""
from os import getenv

from flask import Flask

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
api_host = getenv('HBNB_API_HOST', '0.0.0.0')
api_port = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown(exception):
    """ Commit changes in database """
    storage.close()


if __name__ == '__main__':
    app.run(host=api_host, port=int(api_port), threaded=True)
