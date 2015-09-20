from flask import Flask, jsonify

app = Flask(__name__)

import requests
import json
from lxml import etree
from StringIO import StringIO

@app.route('/api/stats/<username>')
def user_data(username):
    r = requests.get("https://www.periscope.tv/%s/"%(username,))
    parser = etree.HTMLParser()
    doc = etree.parse(StringIO(r.content), parser)
    bcast_data = json.loads(doc.xpath('//meta[@id="broadcast-data"]/@content')[0])
    return jsonify(data=bcast_data)


if __name__ == '__main__':
    app.run(debug=True)
