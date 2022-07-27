#!/usr/bin/env python3
"""This script will create routes for session authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """This function will help user to log in"""
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search()
    try:
        ls = [user for user in users if user.email == email]
        user = ls[0]
        if user.is_valid_password(password):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            resp = make_response(jsonify(user.to_json()))
            resp.set_cookie(getenv('SESSION_NAME'), sess_id)
            return resp
        else:
            return jsonify({"error": "wrong password"}), 401
    except IndexError as e:
        return jsonify({"error": "no user found for this email"}), 404
