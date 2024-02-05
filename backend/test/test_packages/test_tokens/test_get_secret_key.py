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
from backend.packages.tokens.get_secret_key import get_secret_key


@pytest.mark.asyncio
async def test_get_secret_key_000_nominal(monkeypatch):
    """
    Test 000 - Nominal
    Conditions: Environment variable "SECRET_KEY" is set as a string
    Result: Secret key string returned
    """
    monkeypatch.setenv("SECRET_KEY", "This is a secret key.")
    secret_key = get_secret_key()
    assert secret_key == "This is a secret key."


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
