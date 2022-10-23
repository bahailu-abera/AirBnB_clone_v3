#!/usr/bin/python3
"""
View for review objects
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all review objects of a Place
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """
    Retrieves a place object by review_id
    """
    obj = storage.get(classes["Review"], review_id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object
    """
    obj = storage.get(classes["Review"], review_id)

    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """
    Creates a Review
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    if ("user_id" not in json_data):
        abort(400, "Missing user_id")
    user_obj = storage.get(classes["User"], json_data["user_id"])
    if user_obj is None:
        abort(404)
    if ("text" not in json_data):
        abort(400, "Missing text")

    new_review = classes["Review"](place_id=place_id, **json_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """
    Updates Review object
    """
    obj = storage.get(classes["Review"], review_id)
    if obj is None:
        abort(404)
    json_data = request.get_json(force=True, silent=True)
    if (type(json_data) is not dict):
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in json_data.items():
        if key in ignored_keys:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
