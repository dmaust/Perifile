__author__ = 'dmaust'

from perifile import models
from collections import namedtuple

from perifile import db
from lxml import etree
import json
from cStringIO import StringIO
import requests
from sqlalchemy import desc
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

    metrics = models.UserMetrics(
        user_id=user.id,
        time_retrieved=time.time(),
        followers=followers,
        following=following,
        hearts=hearts)

    db.session.add(metrics)
    db.session.commit()
    return metrics

def fetch_user_cached(username):
    subq = db.session.query(models.User.id).filter(models.User.username==username).subquery('u')
    user_metrics = models.UserMetrics\
        .query.filter(models.UserMetrics.user_id.in_(subq))\
        .order_by(desc(models.UserMetrics.time_retrieved))\
        .first()
    ttl = 3600
    if user_metrics is None or (time.time() - user_metrics.time_retrieved) > ttl:
        # Fetch from site.
        return fetch_user_data(username)
    else:
        # Return cached copy
        return user_metrics





