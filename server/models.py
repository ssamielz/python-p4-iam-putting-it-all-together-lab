from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    _password_hash: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String)

    recipes = relationship("Recipe", back_populates="user")

    __table_args__ = (UniqueConstraint("username"),)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be accessed.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be present")
        return username

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    instructions: Mapped[str] = mapped_column(String, nullable=False)
    minutes_to_complete: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="recipes")

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must be present")
        return title

    @validates("instructions")
    def validate_instructions(self, key, instructions):
        if not instructions:
            raise ValueError("Instructions must be present")
        if len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long")
        return instructions
