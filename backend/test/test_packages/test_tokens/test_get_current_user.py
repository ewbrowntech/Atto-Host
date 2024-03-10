"""
tokens/get_current_user.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_current_user.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import jwt
import pytest
from unittest.mock import patch
import secrets
from fastapi import HTTPException
from jose import JWTError
from app.packages.tokens.get_secret_key import get_secret_key
from app.packages.tokens.get_current_user import get_current_user


@pytest.mark.asyncio
async def test_get_current_user_000_nominal(
    monkeypatch, test_db_session, seed_user, seed_jwt
):
    """
    Test 001 - Anomalous
    Conditions: No JWT included
    Result: credentials_exception
    """
    user = await get_current_user(token=seed_jwt, db=test_db_session)
    assert user.username == seed_user.username


@pytest.mark.asyncio
async def test_get_current_user_001_anomalous_no_jwt_provided(
    monkeypatch, test_db_session, seed_user
):
    """
    Test 001 - Anomalous
    Conditions: No JWT included
    Result: credentials_exception
    """
    monkeypatch.setenv("SECRET_KEY", secrets.token_hex(32))
    with pytest.raises(HTTPException) as e:
        user = await get_current_user(token=None, db=test_db_session)
    assert str(e.value) == "401: No JWT included in request"


@pytest.mark.asyncio
async def test_get_current_user_002_anomalous_jwt_indecipherable(
    monkeypatch, test_db_session, seed_user
):
    """
    Test 002 - Anomalous
    Conditions: The provided JWT cannot be decoded
    Result: credentials_exception
    """
    monkeypatch.setenv("SECRET_KEY", secrets.token_hex(32))
    with patch(
        "app.packages.tokens.get_current_user.jwt.decode",
        side_effect=JWTError("Invalid token"),
    ):
        with pytest.raises(HTTPException) as e:
            # Pass a dummy token; it won't be used since jwt.decode is mocked
            user = await get_current_user(
                token="dummy.invalid.token", db=test_db_session
            )
    assert str(e.value) == "401: JWT could not be decoded"


@pytest.mark.asyncio
async def test_get_current_user_003_anomalous_jwt_no_username(
    monkeypatch, test_db_session, seed_user
):
    """
    Test 003 - Anomalous
    Conditions: The decoded JWT does not include a username
    Result: credentials_exception
    """
    monkeypatch.setenv("SECRET_KEY", secrets.token_hex(32))

    # Generate a JWT without a username
    payload = {}
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")

    with pytest.raises(HTTPException) as e:
        user = await get_current_user(token=token, db=test_db_session)
    assert str(e.value) == "401: JWT did not include a username"


@pytest.mark.asyncio
async def test_get_current_user_004_anomalous_jwt_bad_usernamee(
    monkeypatch, test_db_session, seed_user
):
    """
    Test 004 - Anomalous
    Conditions: The decoded JWT does not include a username
    Result: credentials_exception
    """
    monkeypatch.setenv("SECRET_KEY", secrets.token_hex(32))

    # Generate a JWT without a username
    payload = {"username": "test-user2"}
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")

    with pytest.raises(HTTPException) as e:
        user = await get_current_user(token=token, db=test_db_session)
    assert str(e.value) == "401: User specified by JWT does not exist"
