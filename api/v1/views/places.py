#!/usr/bin/python3
"""Defines a new view for Place objects that handles all default RESTFul API
actions"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from flask import request, jsonify, abort, make_response
from models import storage
import requests
import json
from os import getenv


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


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def post_place_search():
    """retrieves all Place objects depending of the JSON in the body of
    the request"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    if not body or (not body.get('states') and
                    not body.get('cities') and
                    not body.get('amenities')):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body.get('states'):
        states = [storage.get("State", id) for id in body.get('states')]
        for state in states:
            for city in state.cities:
                for place in city.places:
                    if place not in places:
                        places.append(place)

    if body.get('cities'):
        cities = [storage.get("City", id) for id in body.get('cities')]
        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body.get('amenities'):
        amens = [storage.get("Amenity", id) for id in body.get('amenities')]

        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        url = "http://{}:{}/api/v1/places/".format(host, port)

        sz = len(places)
        i = 0
        while i < sz:
            place = places[i]
            req = url + place.id + "/amenities"
            resp = requests.get(req)
            resp_j = json.loads(resp.text)
            amn_objs = [storage.get("Amenity", amn['id']) for amn in resp_j]
            for amenity in amens:
                if amenity not in amn_objs:
                    places.pop(i)
                    i -= 1
                    sz -= 1
                    break
            i += 1

    return jsonify([place.to_dict() for place in places])
