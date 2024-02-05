import os

import jwt


def generate_jwt(username: str):
    # Ensure that a username was provided
    if username is None or username == "":
        return ValueError("<username> is None")
    # Ensure that the usern
    if not isinstance(username, str):
        return TypeError("<username> must be a string")
    # Get the secret key from environment variables
    secret_key = os.environ.get("SECRET_KEY")
    if secret_key is None:
        raise EnvironmentError("The environment variable 'SECRET_KEY' is not set")
    payload = {"username": username}
    token = jwt.encode(payload, str(secret_key), algorithm="HS256")
    return token
