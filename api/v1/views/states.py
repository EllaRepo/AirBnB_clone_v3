#!/usr/bin/python3
"""Defines a new view for State objects that handles all default RESTFul API
actions"""
from api.v1.views import app_views
from models.state import State
from flask import request, jsonify, abort, make_response
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_with_id(state_id):
    """Retrieves a State object with state_id"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object with state_id"""
    state = storage.get("State", state_id)
    if state:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State object"""
    state = storage.get("State", state_id)
    if state:
        u_state = request.get_json()
        if u_state:
            for k, v in u_state.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(state, k, v)
            storage.save()
            return make_response(jsonify(state.to_dict()), 200)
        abort(400, "Not a JSON")
    abort(404)
