"""
test_tokens/test_get_secret_key.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_secret_key()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
import os
import secrets
from backend.packages.tokens.get_secret_key import get_secret_key


@pytest.mark.asyncio
async def test_get_secret_key_000_nominal(monkeypatch):
    """
    Test 000 - Nominal
    Conditions: Environment variable "SECRET_KEY" is set as a string
    Result: Secret key string returned
    """
    test_key = secrets.token_hex(32)
    monkeypatch.setenv("SECRET_KEY", test_key)
    secret_key = get_secret_key()
    assert secret_key == test_key


@pytest.mark.asyncio
async def test_get_secret_key_001_anomalous_no_secret_key(monkeypatch):
    """
    Test 001 - Anomalous
    Conditions: Environment variable "SECRET_KEY" is not set
    Result: EnvironmentVariable("The environment variable 'SECRET_KEY' is not set")
    """
    with pytest.raises(EnvironmentError) as e:
        secret_key = get_secret_key()
    assert str(e.value) == "The environment variable 'SECRET_KEY' is not set"


@pytest.mark.asyncio
async def test_get_secret_key_002_anomalous_secret_key_is_empty_string(monkeypatch):
    """
    Test 002 - Anomalous
    Conditions: Environment variable "SECRET_KEY" is an empty string
    Result: ValueError("The environmet variable 'SECRET_KEY' is None")
    """
    monkeypatch.setenv("SECRET_KEY", "")
    with pytest.raises(ValueError) as e:
        secret_key = get_secret_key()
    assert str(e.value) == "The environmet variable 'SECRET_KEY' is None"


@pytest.mark.asyncio
async def test_get_secret_key_003_anomalous_secret_key_is_too_short(monkeypatch):
    """
    Test 003 - Anomalous
    Conditions: environment variable "SECRET_KEY" is a string that is < 256 bits (64 characters) long
    Result: ValueError("Secret key must be at least 256 bits (64 characters) long")
    """
    # Create a key that is 63 characters long, one character short of the requirement
    test_key = secrets.token_hex(31)
    test_key += "a"
    monkeypatch.setenv("SECRET_KEY", test_key)
    with pytest.raises(ValueError) as e:
        secret_key = get_secret_key()
    assert (
        str(e.value)
        == "Secret key must be at least 256 bits (64 hexadecimal characters) long"
    )
