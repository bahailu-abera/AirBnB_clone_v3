#!/usr/bin/python3
"""
View for amenity objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenitys():
    """
    Retrieves the list of all Amenity objects
    """
    objects = storage.all("Amenity")

    list_objs = []
    for obj in objects.values():
        list_objs.append(obj.to_dict())

    return jsonify(list_objs)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves a amenity object by amenity_id
    """
    obj = storage.get(classes["Amenity"], amenity_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object
    """
    obj = storage.get(classes["Amenity"], amenity_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenitys():
    """
    Creates a Amenity
    """
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("name" not in json_data):
        abort(400, "Missing name")

    new_amenity = classes["Amenity"](**json_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates Amenity object
    """
    obj = storage.get(classes["Amenity"], amenity_id)
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
