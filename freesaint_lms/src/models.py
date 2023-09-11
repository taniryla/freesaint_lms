from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class App_Users(db.Model):
    __tablename__ = 'app_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    googleid = db.Column(db.String(128), unique=True)
    gwttoken = db.Column(db.String(128), unique=True)
    profile_active = db.Column(db.Boolean)
    calculated_cal_goal = db.Column(db.Integer)
    starting_weight = db.Column(db.Integer)
    target_weight = db.Column(db.Integer)
    avatar_photo = db.Column(db.JSON)
    target_weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
    
likes_table = db.Table(
    'likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'tweet_id', db.Integer,
        db.ForeignKey('tweets.id'),
        primary_key=True
    ),
    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', nullable=False))

    liking_users = db.relationship(
        'User', secondary=likes_table,
        lazy='subquery',
        backref=db.backref('liked_tweets', lazy=True)
    )
    
    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.content,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }