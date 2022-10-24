#!/usr/bin/python3
"""
View for place objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all place objects of a City
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """
    Retrieves a citie object by place_id
    """
    obj = storage.get(classes["Place"], place_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object
    """
    obj = storage.get(classes["Place"], place_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("user_id" not in json_data):
        abort(400, "Missing user_id")
    user_obj = storage.get(classes["User"], json_data["user_id"])
    if user_obj is None:
        abort(404)
    if ("name" not in json_data):
        abort(400, "Missing name")

    new_place = classes["Place"](city_id=city_id, **json_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """
    Updates Place object
    """
    obj = storage.get(classes["Place"], place_id)
    if obj is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in json_data.items():
        if key in ignored_keys:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def search_places():
    """
    Retrieves all Place objects
    """
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if not data_json or (
            not data_json.get("states") and
            not data_json.get("cities") and
            not data_json.get("amenities")):
        places = storage.all("Place")
        return jsonify([place.to_dict() for place in places.values()])
    places = []

    if ("states" in data_json):
        states = data_json["states"]
        for state_id in states:
            state_obj = storage.get(classes["State"], state_id)
            for city in state_obj.cities:
                city_obj = storage.get(classes["City"], city.id)
                for place in city_obj.places:
                    places.append(place)

    if ("cities" in data_json):
        cities = data_json["cities"]
        for city_id in cities:
            city_obj = storage.get(classes["City"], city_id)
            if city_obj is None:
                continue
            for place in city_obj.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all("Place")
        places = [place for place in places.values()]

    if ("amenities" in data_json):
        amenity_objs = [storage.get(classes["Amenity"], id)
                        for id in data_json["amenities"]]
        i = 0
        length = len(places)
        while i < length:
            for amenity in amenity_objs:
                if amenity not in places[i].amenities:
                    places.pop(i)
                    i -= 1
                    length -= 1
            i += 1
    return jsonify([place.to_dict() for place in places])
