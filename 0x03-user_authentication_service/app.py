#!/usr/bin/env python3
"""This function will create a basic flask app"""

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'])
def basic():
    """This function will return a basic flask app"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
