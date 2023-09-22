#!/usr/bin/python3
""" RESTful api for places review """
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def place_reviews(place_id):
    """ retrive review based on place_id """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for reivew in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def show_review(review_id):
    """ retrive review based on provided review_id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict_())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """delete reive basese on provided review_id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ create review for a given place_id """
    place = storage.get("Place", place_id)
    data = request.get_json()
    if place is None:
        abort(404)
    if type(data) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in data:
        return abort(400, {'message': 'Missing user_id'})
    data['place_id'] = place_id
    user = storage.get("User", data.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in data:
        return abort(400, {'message': 'text'})

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_reviews(review_id):
    """update review based on given review_id"""
    ignored_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ignored_list:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
