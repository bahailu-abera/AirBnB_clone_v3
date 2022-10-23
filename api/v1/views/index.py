"""
Landing page
"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def check_status():
    """
    Check the status of application
    """
    return jsonify({'status': 'OK'})
