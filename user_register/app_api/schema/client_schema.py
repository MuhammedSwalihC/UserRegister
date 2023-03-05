"""Model Schemas."""
from __future__ import annotations

from marshmallow import Schema, ValidationError, fields, validate


def must_not_be_blank(data):
    """function for not blank"""
    if not data:
        raise ValidationError("Data not provided.")


class UserRolesSchema(Schema):
    """user role schema"""
    id = fields.Int(required=False)
    role_name = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.And(validate.Length(max=10)),
    )
    hierarchy_level = fields.Int(required=True)
    is_active = fields.Boolean(dump_only=True)
    is_delete = fields.Boolean(dump_only=True)


class SuperAdminRegistrationSchema(Schema):
    """class sup[er admin schema"""
    id = fields.Int(required=False)
    email = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.And(
            validate.Length(max=100), validate.Regexp(
                r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,10})+$",
            ),
        ),
    )
    password = fields.Str(
        required=False, allow_none=True,
        validate=validate.And(validate.Length(max=150)),
    )
    created_at = fields.String(dump_only=True)
    public_id = fields.Str(dump_only=True)
    user_role_id = fields.Int(required=False)
    user_role = fields.Nested(
        UserRolesSchema,
        validate=must_not_be_blank
        )


class ClientProfileSchema(Schema):
    '''User profile schema'''
    id = fields.Int(required=False)
    full_name = fields.String(
        required=True, allow_none=False,
        validate=validate.Regexp(
            r"^([a-zA-z\s\-\_\.]{2,225})$",
        ),
    )
    country = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r"^([a-zA-z\s\-\_\.]{2,70})$",
        ),
    )
    nationality = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r"^([a-zA-z0-9\s\-\_]{2,225})$",
        ),
    )
    state = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r"^([a-zA-z\s\-\_\.]{2,70})$",
        ),
    )
    user_address = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r"^([a-zA-z0-9\s\-\_\.\,\)\(]{2,225})$",
        ),
    )
    client_id = fields.Str(dump_only=True)
    client = fields.Nested(
        SuperAdminRegistrationSchema,
        validate=must_not_be_blank
    )
    is_delete = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
