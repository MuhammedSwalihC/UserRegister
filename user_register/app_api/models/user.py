"""Class definition for User model."""
from __future__ import annotations
import time
from uuid import uuid4
from app_api import db


def set_created_at():
    """set created time"""
    return round(time.time() * 1000)


class UserModel(db.Model):
    """User model for storing login credentials and other details."""

    __tablename__ = "users_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(255), default=set_created_at)
    public_id = db.Column(
        db.String(100),
        unique=True,
        default=lambda: str(uuid4()),
    )
    is_delete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    user_role_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user_roles.id",
        ),
        nullable=False,
    )
    user_role = db.relationship(
        "UserRoles",
        foreign_keys=[
            user_role_id,
        ],
        backref=db.backref("cilent_user_role", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<User email={self.email}, public_id={self.public_id}>"


class UserProfile(db.Model):
    """user profile model class object"""

    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    nationality = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    user_address = db.Column(db.Text, nullable=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users_table.id",
        ),
        nullable=False,
    )
    client = db.relationship(
        "UserModel",
        foreign_keys=[
            client_id,
        ],
        backref=db.backref("client_ref", lazy="dynamic"),
    )
    is_delete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    reporting_to_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users_table.id",
        ),
        nullable=True,
    )
    reporting_to = db.relationship(
        "UserModel",
        foreign_keys=[
            client_id,
        ],
        backref=db.backref("reporting_to_user", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<UserProfile id={self.id}, full_name={self.full_name}>"


class UserRoles(db.Model):
    """User role setting"""

    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)
    hierarchy_level = db.Column(db.Integer, nullable=False, unique=True)
    is_delete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<UserRoles id={self.id}, role_name={self.role_name}, \
            hierarchy_level={self.hierarchy_level}>"
