"""here we genearting the token"""
import jwt
import datetime
from functools import wraps
import uuid


def create_refresh_token(user_name, compare_value):
    """
    Generates the Acess Token
    :return: string
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            "iat": datetime.datetime.utcnow(),
            "sub": user_name,
            "compare_value": compare_value,
            "token_type": "refresh",
            "fresh": False,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(
            payload, "5f719018ad6dbd0d023614e8956cfdcb7158945a", algorithm="HS256"
        )
    except Exception as err:
        return err


def create_access_token(user_name, compare_value):
    """
    Generates the Refresh Token
    :return: string
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            "iat": datetime.datetime.utcnow(),
            "sub": user_name,
            "compare_value": compare_value,
            "token_type": "access",
            "fresh": False,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(
            payload, "5f719018ad6dbd0d023614e8956cfdcb7158945a", algorithm="HS256"
        )
    except Exception as err:
        return err


def decode_auth_token(access_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        token_payload = jwt.decode(
            access_token,
            "5f719018ad6dbd0d023614e8956cfdcb7158945a",
            algorithms=["HS256"],
        )
        return {"token": token_payload, "code": 200}
    except jwt.ExpiredSignatureError:
        return {"message": "Time is expired, Please register again", "code": 401}
    except jwt.InvalidTokenError:
        return {"message": "Invalid token. Please register again.", "code": 401}
