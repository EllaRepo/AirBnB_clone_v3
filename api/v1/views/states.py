#!/usr/bin/python3
"""
Create a new view for State objects that handles all default
RESTFul API actions:
In the file api/v1/views/states.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, jsonify, abort, request, Response


@app_views.route("states", methods=['GET'], strict_slashes=False)
def get_states():
    """ get all states """
    state_list = []
    all_states = storage.all('State')
    for row in all_states.values():
        state_list.append(row.to_dict())
        return jsonify(state_list)


@app_views.route("states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """ get states based on provided state id """
    state_list = []
    all_states = storage.all('State')
    for key, value in all_states.items():
        if f"State.{state_id}" == Key:
            return jsonify(value.to_dict())
    abort(400)


@app_views.route("states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """ delete states based on id provided """
    state_list = []
    all_states = storage.all('State')
    for key, value in all_states.items():
        if f"State.{state_id}" == Key:
            storage.delete(value)
            storage.save()
            return {}
    abort(400)


@app_views.route("states/<state_id>", methods=['POST'], strict_slashes=False)
def post_states(state_id):
    """ create states based on json date """
    data = request.get_json()
    if data:
        abort(400, "Not a JSON")
    elif "name" not in data:
        abort(400, "Missing name")
    else:
        created_state = State(**request.get_json)
        storage.new(created_state)
        storage.save()
    return created_state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_states(states_id):
    """ update states based on json date """
    obj = storage.get("States", state_id)
    if obj:
        data = request.get_json()
        if isinstance(data, dict):
            ignored = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in obj.items():
                if key not in ignored:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
