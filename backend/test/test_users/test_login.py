"""
tests/test_remove_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for POST /users/login

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from passlib.context import CryptContext
import base64
import secrets

from backend.models.models import User
from backend.routers.users import pwd_context


# Determine if a string is a JWT
def is_jwt(token):
    try:
        # Split the token
        parts = token.split(".")
        if len(parts) == 3:
            # Decode the header to check if it's valid JSON
            header = base64.urlsafe_b64decode(parts[0] + "==")
            # If this doesn't raise an error, it's possibly a JWT
            return True
    except Exception as e:
        # If any error occurs, it's likely not a JWT
        return False


@pytest.mark.asyncio
async def test_login_000_nominal(monkeypatch, client, test_db_session, seed_user):
    """
    Test 000 - Nominal
    Conditions: Correct username and password provided
    Result: JWT returned
    """
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("SECRET_KEY", test_secret_key)

    response = client.post(
        "users/login", json={"username": "test-user", "password": "password"}
    )
    # Refresh the user object to get the current JWT
    await test_db_session.refresh(seed_user)

    assert response.status_code == 200
    jwt = response.json()
    assert is_jwt(jwt)
    assert pwd_context.verify(jwt, seed_user.hashed_token)


@pytest.mark.asyncio
async def test_login_001_anomalous_no_username_provided(client):
    """
    Test 001 - Anomalous
    Conditions: Password provided, but username missing
    Result: {Pydantic error}
    """
    response = client.post("users/login", json={"password": "password"})
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body", "username"]


@pytest.mark.asyncio
async def test_login_002_anomalous_no_password_provided(client):
    """
    Test 002 - Anomalous
    Conditions: Username provided, but password missing
    Result: {Pydantic error}
    """
    response = client.post("users/login", json={"username": "test-user"})
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body", "password"]


@pytest.mark.asyncio
async def test_login_003_anomalous_nonexistent_username(client):
    """
    Test 003 - Anomalous
    Conditions: Username provided does not exist
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    response = client.post(
        "users/login", json={"username": "test-user", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "The provided credentials were incorrect"


@pytest.mark.asyncio
async def test_login_004_anomalous_incorrect_password(client, test_db_session):
    """
    Test 004 - Anomalous
    Conditions: Incorrect password provided
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Create a test user
    hashed_password = pwd_context.hash("password")
    user = User(username="test-user", hashed_password=hashed_password)
    test_db_session.add(user)

    response = client.post(
        "users/login", json={"username": "test-user", "password": "incorrect-password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "The provided credentials were incorrect"
