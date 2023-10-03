#!/usr/bin/python3
"""Defines a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, make_response
from models import storage
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """Retrieves the list of all all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            ams = [amenity.to_dict() for amenity in place.amenities]
        else:
            ams = [storage.get(Amenity, id).to_dict() for id in
                   place.amenity_ids]
        return jsonify(ams)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                if amenity not in place.amenities:
                    abort(404)
            else:
                if amenity_id not in place.amenity_ids:
                    abort(404)
                index = place.amenity_ids.index(amenity_id)
                place.amenity_ids.pop(index)
            amenity.delete()
            storage.save()
            return make_response(jsonify({}), 200)
        abort(404)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                if amenity in place.amenities:
                    return make_response(jsonify(amenity.to_dict()), 200)
                place.amenities.append(amenity)
            else:
                if amenity_id in place.amenity_ids:
                    return make_response(jsonify(amenity.to_dict()), 200)
                place.amenity_ids.append(amenity_id)
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        abort(404)
    abort(404)
