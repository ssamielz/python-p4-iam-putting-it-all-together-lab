from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    @property
    def password_hash(self):
        raise AttributeError('password_hash is write-only')

    @password_hash.setter
    def password_hash(self, plain):
        self._password_hash = bcrypt.generate_password_hash(plain).decode()

    def authenticate(self, plain):
        return bcrypt.check_password_hash(self._password_hash, plain)

    @validates('username')
    def validate_username(self, key, u):
        if not u:
            raise ValueError("Username required")
        return u

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('instructions')
    def validate_instructions(self, key, inst):
        if not inst or len(inst) < 50:
            raise ValueError("Instructions must be 50+ chars")
        return inst

    @validates('title')
    def validate_title(self, key, t):
        if not t:
            raise ValueError("Title required")
        return t
