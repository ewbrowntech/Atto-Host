"""
tests/test_remove_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for removing files in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest

from sqlalchemy import select

from app.models.models import File as FileModel
from app.packages.storage_driver.is_file_present import is_file_present

from test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_remove_file_000_nominal_file_present_owner(
    monkeypatch,
    client,
    test_db_session,
    seed_jwt,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 000 - Nominal
    Conditions: File object present and file present in storage, request is from file owner
    Result: HTTP 204 - No content
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_jwt}"}
    response = client.delete("files/abcdefgh", headers=headers)
    assert response.status_code == 204

    # Validate that the file object has been deleted
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []

    # Validate that the file itself has been deleted
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_file_001_nominal_file_present_admin(
    monkeypatch,
    client,
    test_db_session,
    seed_admin_jwt,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 001 - Nominal
    Conditions: File object present and file present in storage, request is from admin
    Result: HTTP 204 - No content
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_admin_jwt}"}
    response = client.delete("files/abcdefgh", headers=headers)
    assert response.status_code == 204

    # Validate that the file object has been deleted
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []

    # Validate that the file itself has been deleted
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_file_002_anomalous_nonexistent_file(
    monkeypatch, client, seed_jwt, seed_file_binary, clear_storage_directory
):
    """
    Test 001 - Anomalous
    Conditions: File object is not present in database
    Result: HTTP 204 - No content
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_jwt}"}
    response = client.delete("files/abcdefgh", headers=headers)
    assert response.status_code == 404

    # Validate that the file binary is NOT deleted
    assert is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_file_003_anomalous_file_missing_in_storage(
    monkeypatch,
    client,
    test_db_session,
    seed_jwt,
    seed_file_object,
    clear_storage_directory,
):
    """
    Test 002 - Anomalous
    Conditions: File object in database but file itself not in storage
    Result: HTTP 204 - No content
    """
    """
    Test 000 - Nominal
    Conditions: File object present and file present in storage
    Result: HTTP 204 - No content
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_jwt}"}
    response = client.delete("files/abcdefgh", headers=headers)
    assert response.status_code == 204

    # Validate that the file object has been deleted
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []

    # Validate that the file itself has been deleted
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_file_004_anomalous_file_insufficient_priveledges(
    monkeypatch,
    client,
    test_db_session,
    seed_file_object,
    seed_file_binary,
    seed_jwt2,
    clear_storage_directory,
):
    """
    Test 004 - Anomalous
    Conditions: The requester is neither the file owner nor an admin
    Result: HTTP 403 - "The current user is not authorized to perform this action"
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_jwt2}"}
    response = client.delete("files/abcdefgh", headers=headers)
    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "The current user is not authorized to perform this action"
    )
    # Validate that the file object has NOT been deleted
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert len(files) == 1

    # Validate that the file itself has NOT been deleted
    assert is_file_present("abcdefgh.jpeg")
