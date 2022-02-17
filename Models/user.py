from werkzeug.security import generate_password_hash, check_password_hash

from db import db


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    country = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(100))

    def __init__(self, name, surname, email, country, is_admin=False):
        self.name = name
        self.surname = surname
        self.email = email
        self.country = country
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.title