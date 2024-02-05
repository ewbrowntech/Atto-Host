import os
import jwt
from backend.packages.tokens.get_secret_key import get_secret_key


def generate_jwt(username: str):
    # Ensure that a username was provided
    if username is None or username == "":
        return ValueError("<username> is None")
    # Ensure that <username> is a string
    if not isinstance(username, str):
        return TypeError("<username> must be a string")
    payload = {"username": username}
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")
    return token
