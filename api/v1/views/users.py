#!/usr/bin/python3
"""Implementation of RESTful api for users"""
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, abort, make_response
from models import storage


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def users():
    """return all users """
    users = storage.all(User).values()
    if users is None:
        abort(404)
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def show_user(user_id):
    """Return users based on user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user based on provided user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def insert_user():
    """insert new user for a given user id"""

    data = request.get_json()
    if type(data) != dict:
        abort(400, description="Not a JSON")
    if not data.get("email"):
        abort(400, description="Missing email")
    if not data.get("password"):
        abort(400, description="Missing password")
    new_user = City(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update city based on given city_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
