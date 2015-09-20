from flask import Flask, jsonify, render_template

from perifile import app
from perifile import common

import re

@app.route('/api/stats/<username>')
def user_data(username):
    metrics = common.fetch_user_cached(username)
    return jsonify(metrics=metrics.to_dict())

@app.route('/profile/<username>')
def profile_page(username):
    metrics = common.fetch_user_cached(username)

    pattern = re.compile('^[A-Za-z0-9]*$')
    if not pattern.match(username):
        return "Invalid username"

    return render_template("profile.html", username=username, **metrics.to_dict())