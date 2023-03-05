from __future__ import annotations
from flask import jsonify, request
from app_api.utils.save import global_save
from app_api.models.user import UserModel, UserProfile, UserRoles
from app_api.schema import client_schema
import uuid
from app_api.utils.filter import model_filter
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
import random
import math
from app_api.utils.exception_handler import SchemaValidator


def register_superadmin():
    """register super admin"""
    request_body = request.get_json()
    validate_data = SchemaValidator(response=request_body).isTrue(
        client_schema.SuperAdminRegistrationSchema()
    )
    if isinstance(validate_data, tuple):
        return validate_data
    public_id = str(uuid.uuid4())
    validate_data["public_id"] = public_id
    validate_data["is_active"] = True
    validate_data["is_delete"] = False
    admin_obj = global_save(UserModel(), validate_data)
    validate_data.pop("public_id")
    validate_data["client_id"] = admin_obj.id
    _ = global_save(UserProfile(), validate_data)
    return client_schema.SuperAdminRegistrationSchema().dump(admin_obj)


def get_all_clients():
    """get all admins"""
    request_instance = request.get_json()
    paging = request_instance.get("paging", {"page": 1, "per_page": 10})
    columns = request_instance.get("columns", ["id"])
    form = dict(
        is_delete=False,
        is_active=True,
    )
    filter = {"opr": "eq", "value": form, "paging": paging, "columns": columns}
    query = model_filter(UserModel, filter)
    instance = client_schema.SuperAdminRegistrationSchema(
        many=True,
    ).dump(query.get("items", []))
    query["items"] = instance
    return query


def otp_string():
    """generate 6 didgit number"""
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


def super_admin_login():
    """admin login"""
    request_body = request.get_json()
    email = request_body.get("email", None)
    password = request_body.get("password", None)
    form = dict(
        email=email,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserModel, filter)["items"][0]
    client_user = client_schema.SuperAdminRegistrationSchema().dump(query)
    if client_user["password"] != password:
        return jsonify(status="Failed", response="incorrect password")
    random_six_digit_code = otp_string()
    form_pro = dict(
        client_id=client_user["id"],
    )
    filter_pro = {"opr": "eq", "value": form_pro}
    query_pro = model_filter(UserProfile, filter_pro)
    user_profile = client_schema.ClientProfileSchema().dump(query_pro.get("items")[0])
    company_name = user_profile.get("company_name", "Lanware Solutions")
    refresh_token = create_refresh_token(
        identity={
            "email": query.email,
            "compare_value": random_six_digit_code,
            "public_id": query.public_id,
            "user_role": query.user_role.id,
            "company_name": company_name,
        }
    )
    access_token = create_access_token(
        identity={
            "email": query.email,
            "compare_value": random_six_digit_code,
            "public_id": query.public_id,
            "user_role": query.user_role.id,
            "company_name": company_name,
        }
    )
    return jsonify(refresh_token=refresh_token, access_token=access_token)


@jwt_required()
def create_user():
    """add users"""
    identity = get_jwt_identity()
    request_body = request.get_json()
    user_role_id = request_body.get("user_role_id", None)
    if user_role_id is 1:
        return dict(
            status="Failed", message="No Permission to add users as Super Admin"
        )
    if user_role_id is None:
        return dict(status="Failed", message="Please provide Role")
    if identity.get("user_role", None) is 5:
        return dict(status="Failed", message="No Permission to add users")
    validate_data = SchemaValidator(response=request_body).isTrue(
        client_schema.SuperAdminRegistrationSchema()
    )
    if isinstance(validate_data, tuple):
        return validate_data
    public_id = str(uuid.uuid4())
    validate_data["public_id"] = public_id
    validate_data["is_active"] = True
    validate_data["is_delete"] = False
    admin_obj = global_save(UserModel(), validate_data)
    validate_data.pop("public_id")
    validate_data["client_id"] = admin_obj.id
    _ = global_save(UserProfile(), validate_data)
    return client_schema.SuperAdminRegistrationSchema().dump(admin_obj)


@jwt_required(refresh=True)
def refresh_users_token():
    """refresh token"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_required()
def update_clientprofile(_id):
    """Update contact"""
    request_body = request.get_json()
    validate_data = SchemaValidator(response=request_body).isTrue(
        client_schema.ClientProfileSchema()
    )
    if isinstance(validate_data, tuple):
        return validate_data
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserProfile, filter)
    if query["items"]:
        updated_user_details = global_save(query["items"][0], validate_data)
        return client_schema.ClientProfileSchema().dump(updated_user_details)
    return jsonify(status="Failed", message="Failed to save")


@jwt_required()
def profile_update_by_field(_id):
    """Update contact"""
    data = request.get_json()
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserProfile, filter)
    if query["items"]:
        updated_user_details = global_save(query["items"][0], data)
        return client_schema.ClientProfileSchema().dump(updated_user_details)
    return jsonify(status="Failed", message="Failed to save")


@jwt_required()
def get_client_profile(_id):
    """get Client profile by id"""
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserProfile, filter)
    if query["items"]:
        return client_schema.ClientProfileSchema().dump(query["items"][0])
    return client_schema.ClientProfileSchema().dump(query["items"])


####################### user Role ###################################


@jwt_required()
def create_user_role():
    """create_user_role"""
    identity = get_jwt_identity()
    if identity.get("user_role", None) is 1:
        request_body = request.get_json()

        validate_data = SchemaValidator(response=request_body).isTrue(
            client_schema.UserRolesSchema()
        )
        if isinstance(validate_data, tuple):
            return validate_data
        validate_data["created_by_id"] = identity.get("public_id")
        validate_data["is_active"] = True
        validate_data["is_delete"] = False
        role_ob = global_save(UserRoles(), validate_data)
        return client_schema.UserRolesSchema().dump(role_ob)
    return jsonify(status="Failed", message="You have No access")


@jwt_required()
def get_all_roles():
    """"""
    request_instance = request.get_json()
    paging = request_instance.get("paging", {"page": 1, "per_page": 10})
    columns = request_instance.get("columns", ["id"])
    form = dict(
        is_delete=False,
        is_active=True,
    )
    filter = {"opr": "eq", "value": form, "paging": paging, "columns": columns}
    query = model_filter(UserRoles, filter)
    instance = client_schema.UserRolesSchema(
        many=True,
    ).dump(query.get("items", []))
    query["items"] = instance
    return query


@jwt_required()
def update_user_role(_id):
    """Update contact"""
    request_body = request.get_json()
    validate_data = SchemaValidator(response=request_body).isTrue(
        client_schema.UserRolesSchema()
    )
    if isinstance(validate_data, tuple):
        return validate_data
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserRoles, filter)
    if query["items"]:
        updated_user_details = global_save(query["items"][0], validate_data)
        return client_schema.UserRolesSchema().dump(updated_user_details)
    return jsonify(status="Failed", message="Failed to save")


@jwt_required()
def update_user_by_field(_id):
    """Update contact"""
    data = request.get_json()
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserRoles, filter)
    if query["items"]:
        updated_user_details = global_save(query["items"][0], data)
        return client_schema.UserRolesSchema().dump(updated_user_details)
    return jsonify(status="Failed", message="Failed to save")


@jwt_required()
def get_user_role(_id):
    """get Client profile by id"""
    form = dict(
        id=_id,
    )
    filter = {"opr": "eq", "value": form}
    query = model_filter(UserRoles, filter)
    if query["items"]:
        return client_schema.UserRolesSchema().dump(query["items"][0])
    return client_schema.UserRolesSchema().dump(query["items"])
