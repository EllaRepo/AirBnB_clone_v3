#!/usr/bin/python3
"""Defines a new view for Place objects that handles all default RESTFul API
actions"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from flask import request, jsonify, abort, make_response
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get("City", city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_with_id(place_id):
    """Retrieves place object with place_id"""
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes place object with amenity_id"""
    place = storage.get("Place", place_id)
    if place:
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")
    if not storage.get("User", body["user_id"]):
        abort(404)
    if "name" not in body:
        abort(400, "Missing name")
    place = Place(**body)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates Place object"""
    place = storage.get("Place", place_id)
    if place:
        u_place = request.get_json()
        if u_place:
            for k, v in u_place.items():
                if k not in ["id", "created_at", "updated_at", "user_id",
                             "city_id"]:
                    setattr(place, k, v)
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
        abort(400, "Not a JSON")
    abort(404)
