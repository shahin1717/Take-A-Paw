# app/models.py
from datetime import datetime,timezone
from .db import db

from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    public_contact = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Cascade deletes pets and favorites when user is deleted
    pets = db.relationship("Pet", backref="owner", lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship("Favorite", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(30), nullable=False)
    breed = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    adopted = db.Column(db.Boolean, default=False, nullable=False)
    source = db.Column(db.String(30), default="catalog", nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    contact_email_override = db.Column(db.String(120), nullable=True)
    contact_phone_override = db.Column(db.String(50), nullable=True)

    home_type = db.Column(db.String(50), nullable=True)
    activity_level = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    time_commitment = db.Column(db.String(50), nullable=True)
    family_situation = db.Column(db.String(50), nullable=True)
    public_contact = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Cascade delete favorites when pet is deleted
    favorited_by = db.relationship("Favorite", backref="pet", lazy=True, cascade="all, delete-orphan")


class Favorite(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
