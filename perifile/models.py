__author__ = 'dmaust'

from perifile import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)

    users = db.relationship('UserMetrics', backref="user")

class UserMetrics(db.Model):
    __tablename__ = "user_metrics"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    time_retrieved = db.Column(db.Integer, primary_key=True)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    hearts = db.Column(db.Integer)

    def to_dict(self):
        return {"followers": self.followers, "following": self.following, "hearts": self.hearts}

