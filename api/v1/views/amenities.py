#!/usr/bin/python3
"""Defines a new view for Amenity objects that handles all default RESTFul API
actions"""
from api.v1.views import app_views
from models.amenity import Amenity
from flask import request, jsonify, abort, make_response
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    objs = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_with_id(amenity_id):
    """Retrieves amenity object with amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity object with amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        u_amenity = request.get_json()
        if u_amenity:
            for k, v in u_amenity.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(amenity, k, v)
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 200)
        abort(400, "Not a JSON")
    abort(404)
