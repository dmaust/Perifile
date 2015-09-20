from flask import Flask, jsonify

app = Flask(__name__)

import requests
import json
from perifile import common
from StringIO import StringIO

@app.route('/api/stats/<username>')
def user_data(username):
    metrics = common.fetch_user_data(username)
    return jsonify(metrics=metrics.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
