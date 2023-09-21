#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default
RESTFul API actions:

In the file api/v1/views/amenities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Amenity objects: GET /api/v1/amenities

Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Amenity: POST /api/v1/amenities

You must use request.get_json from Flask to transform the HTTP
request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error
with the message Not a JSON
If the dictionary doesn’t contain the key name, raise a 400 error
with the message Missing name
Returns the new Amenity with the status code 201
Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a
404 error
You must use request.get_json from Flask to transform the HTTP
request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error
with the message Not a JSON
Update the Amenity object with all key-value pairs of the dictionary
Ignore keys: id, created_at and updated_at
Returns the Amenity object with the status code 200
"""
from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    all_states = storage.get(State, state_id)
    if all_states:
        return jsonify([city.to_dict() for city in State.cities])
    abort(404)


@app_views.route("cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_with_id(city_id):
    """ get city based on city_id """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ delete city based on city_id """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_states(state_id):
    """ create new city based on state_id """
    data = request.jsonify()
    state = storage.get(State, state_id)
    if typ(data) != dict:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    if state is None:
        abort(404)
    new_city = City(**data)

    storage.new(new_city)
    new_city.state_id = state_id
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ update city based on city_id """
    city = storage.get(City, city_id)
    data = request.get_json()
    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    if city is None:
        abort(404)
    if type(data) != dict:
        abort(400, description="Not a JSON")
    for key, value data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
