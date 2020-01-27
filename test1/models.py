from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, email, password, name, created_at, last_login):
        self.email = email
        self.password = password
        self.name = name
        self.created_at = created_at
        self.last_login = last_login

    def __repr__(self):
        return '<id {}>'.format(self.id)
