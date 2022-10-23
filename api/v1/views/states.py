#!/usr/bin/python3
"""
View for state objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects
    """
    objects = storage.all("State")

    list_objs = []
    for obj in objects.values():
        list_objs.append(obj.to_dict())

    return jsonify(list_objs)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """
    Retrieves a state object by state_id
    """
    obj = storage.get(classes["State"], state_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object
    """
    obj = storage.get(classes["State"], state_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_states():
    """
    Creates a State
    """
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("name" not in json_data):
        abort(400, "Missing name")

    new_state = classes["State"](**json_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    Updates State object
    """
    obj = storage.get(classes["State"], state_id)
    if obj is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in json_data.items():
        if key in ignored_keys:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
