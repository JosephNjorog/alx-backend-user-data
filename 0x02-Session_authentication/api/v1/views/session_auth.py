#!/usr/bin/env python3
""" Module of session_auth views
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import environ


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """ Login user & set session cookie
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if (password is None) or (password == ""):
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
        assert (type(users) == list) and (len(users) == 1)
    except (KeyError, AssertionError):
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "Error occured"}), 500
    response = jsonify(user.to_json())
    response.set_cookie(environ.get("SESSION_NAME", "set_cookie"), session_id)
    return response


@app_views.route("/auth_session/logout",
                 methods=["DELETE"],
                 strict_slashes=False)
def logout_user() -> str:
    """ Log out user by destroying session ID
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
