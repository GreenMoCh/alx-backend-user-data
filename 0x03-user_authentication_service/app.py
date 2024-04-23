#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
