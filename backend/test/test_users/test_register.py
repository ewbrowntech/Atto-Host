"""
tests/test_remove_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for POST /users/register

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest


@pytest.mark.asyncio
async def test_register_000_nominal(client, test_db_session):
    """
    Test 000 - Nominal
    Conditions: Unique username and password provided
    Result: HTTP 200 - User {username} created
    """
    response = client.post(
        "users/register", json={"username": "test-user", "password": "password"}
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "User test-user created"


@pytest.mark.asyncio
async def test_register_001_anomalous_no_username_provided(client, test_db_session):
    """
    Test 001 - Anomalous
    Conditions: Password provided, but no username provided
    Result: HTTP 422 - {Pydantic error}
    """
    response = client.post("users/register", json={"password": "password"})
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body", "username"]


@pytest.mark.asyncio
async def test_register_002_anomalous_no_password_provided(client, test_db_session):
    """
    Test 002 - Anomalous
    Conditions: Username provided, but no password provided
    Result: HTTP 422 - {Pydantic error}
    """
    response = client.post("users/register", json={"username": "test-user"})
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body", "password"]


@pytest.mark.asyncio
async def test_register_003_anomalous_username_taken(client, test_db_session):
    """
    Test 003 - Anomalous
    Conditions: Non-unique username already registered
    Result: HTTP 400 - Username {username} is already taken
    """
    client.post(
        "users/register", json={"username": "test-user", "password": "password"}
    )
    response = client.post(
        "users/register", json={"username": "test-user", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username test-user is already taken"
