#!/usr/bin/python3
"""
View for citie objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all Citie objects of a State
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """
    Retrieves a citie object by city_id
    """
    obj = storage.get(classes["City"], city_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object
    """
    obj = storage.get(classes["City"], city_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("name" not in json_data):
        abort(400, "Missing name")

    new_city = classes["City"](state_id=state_id, **json_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Updates City object
    """
    obj = storage.get(classes["City"], city_id)
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
