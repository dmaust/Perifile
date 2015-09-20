__author__ = 'dmaust'

from perifile import models
from collections import namedtuple

from perifile import db
from lxml import etree
import json
from cStringIO import StringIO
import requests

import time

def fetch_user_data(username):
    r = requests.get("https://www.periscope.tv/%s/"%(username,))
    parser = etree.HTMLParser()
    doc = etree.parse(StringIO(r.content), parser)
    bcast_data = json.loads(doc.xpath('//meta[@id="broadcast-data"]/@content')[0])
    followers = bcast_data['user']['n_followers']
    following = bcast_data['user']['n_following']
    hearts = bcast_data['user']['n_hearts']

    user = models.User.query.filter_by(username=username).first()
    if user is None:
        user = models.User(username=username)
        db.session.add(user)
        db.session.flush()

    metrics = models.UserMetrics(user_id=user.id, time_retrieved=time.time(), followers=followers, following=following, hearts=hearts)
    db.session.add(metrics)
    db.session.commit()
    return metrics



