#!/usr/bin/python3
"""Create a new view for User objects"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users():
    """return all users """
    my_users = [
        user.to_dict() for user in storage.all(User).values()
    ]
    return make_response(jsonify(my_users), 200)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    """Return users based on user_id"""
    res = storage.get("User", user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user based on provided user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def insert_user():
    """insert new user for a given user id"""
    data = request.get_json()
    if type(data) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in data:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in data:
        return abort(400, {'message': 'Missing password'})
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """update city based on given city_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
