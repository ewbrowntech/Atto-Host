"""
tokens/get_secret_key.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the secret key from environment variables

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import os


def get_secret_key():
    secret_key = os.environ.get("SECRET_KEY")
    if secret_key is None:
        raise EnvironmentError("The environment variable 'SECRET_KEY' is not set")
    if secret_key == "":
        raise ValueError("The environment variable 'SECRET_KEY' is None")
    if len(secret_key) < 64:
        raise ValueError(
            "Secret key must be at least 256 bits (64 hexadecimal characters) long"
        )
    return secret_key
