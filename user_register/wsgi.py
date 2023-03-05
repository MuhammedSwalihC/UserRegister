"""main file"""
from __future__ import annotations
import os

from flask import request
from app_api import create_app, db
from app_api.bussiness import client_bussiness
from app_api.models.user import UserModel, UserRoles, UserProfile

application = create_app(os.getenv("FLASK_ENV", "production"))


@application.shell_context_processor
def shell():
    """custom shell imports"""
    return {
        "db": db,
        "UserModel": UserModel,
        "UserProfile": UserProfile,
        "UserRoles": UserRoles,
    }


@application.route("/super_admin_register", methods=["POST", "GET"])
def super_admin_register():
    "Register Super Admin"
    if request.method == "POST":
        return client_bussiness.register_superadmin()
    elif request.method == "GET":
        return client_bussiness.get_all_clients()
    return dict(status="Failed", message="Method Not Allowed")


@application.route("/admin_login", methods=["POST"])
def admin_login():
    "admin_login"
    if request.method == "POST":
        return client_bussiness.super_admin_login()
    return dict(status="Failed", message="Method Not Allowed")

@application.route("/add_user", methods=["POST"])
def add_user():
    "admin_login"
    if request.method == "POST":
        return client_bussiness.create_user()
    return dict(status="Failed", message="Method Not Allowed")


@application.route("/token/refresh", methods=["GET"])
def refresh_token():
    """get refresh token from access token"""
    if request.method == "GET":
        return client_bussiness.refresh_users_token()
    return dict(status="Failed", message="Method Not Allowed")

@application.route("/client_profile_modify/<int:_id>", methods=["GET","PUT","PATCH"])
def client_profile_modified(_id):
    """client_profile_modified"""
    if request.method == "PUT":
        return client_bussiness.update_clientprofile(_id)
    elif request.method == "PATCH":
        return client_bussiness.profile_update_by_field(_id)
    elif request.method == "GET":
        return client_bussiness.get_client_profile(_id)
    return dict(status="Failed", message="Method Not Allowed")


@application.route("/user_roles", methods=["POST", "GET"])
def user_roles():
    "create user role"
    if request.method == "POST":
        return client_bussiness.create_user_role()
    elif request.method == "GET":
        return client_bussiness.get_all_roles()
    return dict(status="Failed", message="Method Not Allowed")

if __name__ == "__main__":
    application.run(threaded=True, debug=True)
