#!/usr/bin/env python3
"""This function will create a basic flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def basic():
    """This function will return a basic flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    """This function will register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """This route will help user log in"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """This route will delete a user"""
    cookie_value = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(cookie_value)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('basic'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """This route will get user from cookie"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_token():
    """This route will add token to user"""
    try:
        email = request.form.get('email')
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError as e:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """This route will update a password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
