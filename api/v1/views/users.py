#!/usr/bin/python3
"""
View for user objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects
    """
    objects = storage.all("User")

    list_objs = []
    for obj in objects.values():
        list_objs.append(obj.to_dict())

    return jsonify(list_objs)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """
    Retrieves a user object by user_id
    """
    obj = storage.get(classes["User"], user_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object
    """
    obj = storage.get(classes["User"], user_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_users():
    """
    Creates a User
    """
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("email" not in json_data):
        abort(400, "Missing email")
    if ("password" not in json_data):
        abort(400, "Missing password")

    new_user = classes["User"](**json_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    Updates User object
    """
    obj = storage.get(classes["User"], user_id)
    if obj is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    ignored_keys = ["id", "email", "created_at", "updated_at"]

    for key, value in json_data.items():
        if key in ignored_keys:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
