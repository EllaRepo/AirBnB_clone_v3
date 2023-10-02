#!/usr/bin/python3
"""Create a new view for place amenities objects """
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage
from os import getenv
from flask import jsonify, abort, make_response

mode = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities_from_place(place_id):
    """Return amenities based on provided place_id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if mode == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get("Amenity", _id).to_dict() for _id in place.amenity_ids
        ])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Delete amenity_id of a given place_id"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def insert_amenity_in_place(place_id, amenity_id):
    """Add new amienity for a given place based on a given place_id"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)
    if mode == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity.id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
