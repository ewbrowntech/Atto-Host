import os
import jwt
import datetime
from backend.packages.tokens.get_secret_key import get_secret_key


def generate_jwt(username: str):
    # Ensure that a username was provided
    if username is None or username == "":
        raise ValueError("<username> is None")
    # Ensure that <username> is a string
    if not isinstance(username, str):
        raise TypeError(
            f"<username> must be of type <class 'str'>, not {type(username)}"
        )
    payload = {"username": username}
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")
    return token
