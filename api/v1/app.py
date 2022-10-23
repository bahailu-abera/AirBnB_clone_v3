#!/usr/bin/python3
"""
Application logic
"""
from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")
api_host = getenv('HBNB_API_HOST', '0.0.0.0')
api_port = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown(exception):
    """ Commit changes in database """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    resp = {
        'error': 'Not found'
        }
    return jsonify(resp), 404


if __name__ == '__main__':
    app.run(host=api_host, port=int(api_port), threaded=True)
