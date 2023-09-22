#!/usr/bin/python3
""" RESTful api for places review """
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review_by_place(place_id):
    """ retrive review based on place_id """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def show_review(review_id):
    """ retrive review based on provided review_id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


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
def insert_review(place_id):
    """ create review for a given place_id """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if not data.get("user_id"):
        return abort(400, {'message': 'Missing user_id'})
    data['place_id'] = place_id
    user = storage.get("User", data.get('user_id'))
    if user is None:
        abort(404)
    if not data.get("text"):
        return abort(400, {'message': 'text'})
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """update review based on given review_id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
