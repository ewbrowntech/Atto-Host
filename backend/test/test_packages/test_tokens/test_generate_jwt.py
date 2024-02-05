"""
test_tokens/test_generate_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of generate_jwt()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
import secrets
from backend.packages.tokens.generate_jwt import generate_jwt


@pytest.mark.asyncio
async def test_generate_jwt_000_anomalous_no_username(monkeypatch):
    """
    Test 000 - Anomalous
    Conditions: No username provided
    Result: ValueError("<username> is None")
    """
    test_secret_key = secrets.token_hex(31)
    monkeypatch.setenv("SECRET_KEY", test_secret_key)

    test_username = None
    with pytest.raises(ValueError) as e:
        jwt = generate_jwt(test_username)
    assert str(e.value) == "<username> is None"


@pytest.mark.asyncio
async def test_generate_jwt_001_anomalous_username_is_not_a_string(monkeypatch):
    """
    Test 001 - Anomalous
    Conditions: Provided username is an integer, not a string
    Result: TypeError("<username> must be of type <class 'str'>, not <class 'int'>")
    """
    test_secret_key = secrets.token_hex(31)
    monkeypatch.setenv("SECRET_KEY", test_secret_key)

    test_username = 9
    with pytest.raises(TypeError) as e:
        jwt = generate_jwt(test_username)
    assert str(e.value) == "<username> must be of type <class 'str'>, not <class 'int'>"
