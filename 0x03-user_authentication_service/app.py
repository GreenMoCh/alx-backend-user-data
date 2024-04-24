#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, request, jsonify, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Route to return a JSON payload"""
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'])
def users():
    """
    Endpoint to register a new user
    """
    try:
        email = request.form['email']
        password = request.form['password']

        user = AUTH.register_user(email, password)
        response = {
            "email": user.email,
            "message": "user created"
        }
        return jsonify(response), 200
    except ValueError as err:
        response = {"message": str(err)}
        return jsonify(response), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Login route to create a new session for the user
    """
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
    
    return "Unauthorized", 401


@app.route("/sessions", methods=['DELETE'])
def logout():
    """
    Logout route
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")

    return "Forbidden", 403


@app.route("/profile")
def profile():
    """
    Get data of user profile
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user =  AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    
    return "Forbiden", 403


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    if request.method == "POST":
        data = request.form
        if "email" not in data:
            abort(400)

        email = data["email"]
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": reset_token}), 200
        except ValueError as e:
            abort(403, str(e))


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
    Update password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
