#!/usr/bin/python3
"""
View for amenity objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities(place_id):
    """
    Retrieves the list of all amenity objects of a Place
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    amenities_list = []
    for amenity in place.amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_place(place_id, amenity_id):
    """
    Deletes a Amenity object
    """
    place_objs = storage.get(classes["Place"], place_id)
    if place_objs is None:
        abort(404)
    amenity_objs = storage.get(classes["Amenity"], amenity_id)

    if amenity_objs is None:
        abort(404)
    if amenity_objs not in place_objs.amenities:
        abort(404)
    storage.delete(amenity_objs)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_amenity(place_id, amenity_id):
    """
    Creates a Amenity
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    return jsonify(amenity.to_dict()), 201
