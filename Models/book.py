from auth import JWToken
from functools import wraps
from flask import request

from db import db
from Models.user import User


class Book(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    pages = db.Column(db.Integer)

    def __init__(self, name, author, pages):
        self.name = name
        self.author = author
        self.pages = pages

    def __repr__(self):
        return '<User %s>' % self.title


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = JWToken(request.headers)
            user = token.decode_token("random string")
            current_user = User.query.filter_by(id=user['id']).first()
            if not current_user or not user["is_admin"]:
                raise Exception("Access denied!")
        except Exception as e:
            return {
                       "message": str(e),
                       "data": None,
                       "error": "Unauthorized access"
                   }, 401

        return f(*args, **kwargs)

    return decorator
