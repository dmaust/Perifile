from flask import Flask, jsonify

from perifile import app
from perifile import common

@app.route('/api/stats/<username>')
def user_data(username):
    metrics = common.fetch_user_cached(username)
    return jsonify(metrics=metrics.to_dict())


