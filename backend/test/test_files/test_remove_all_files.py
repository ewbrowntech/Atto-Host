"""
tests/test_list_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the files router in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from sqlalchemy import select
from backend.packages.storage_driver.is_file_present import is_file_present
from backend.models.models import File as FileModel
from backend.test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_remove_all_files_000_nominal_no_files_present(
    monkeypatch, client, test_db_session, seed_admin_jwt
):
    """
    Test 000 - Nominal
    Conditions: No files present in database or storage
    Result: HTTP 204 - No content - Nothing happens
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_admin_jwt}"}
    response = client.delete("files/", headers=headers)

    assert response.status_code == 204

    # Validate that the file table is empty
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_all_files_001_nominal_files_present(
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
    Conditions: File present in database and storage
    Result: HTTP 204 - No Content - File removed from database and storage
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_admin_jwt}"}
    response = client.delete("files/", headers=headers)
    assert response.status_code == 204
    # Validate that the file table is empty
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_all_files_002_anomalous_file_in_db_and_not_in_storage(
    monkeypatch,
    client,
    test_db_session,
    seed_admin_jwt,
    seed_file_object,
    clear_storage_directory,
):
    """
    Test 002 - Anomalous
    Conditions: File present in database, but not in storage
    Result: HTTP 204 - No Content - File removed from database
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_admin_jwt}"}
    response = client.delete("files/", headers=headers)
    assert response.status_code == 204
    # Validate that the file table is empty
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_all_files_003_anomalous_file_not_in_db_and_in_storage(
    monkeypatch,
    client,
    test_db_session,
    seed_admin_jwt,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 003 - Anomalous
    Conditions: File present not in database, but is in storage
    Result: HTTP 204 - No Content - File removed from storage
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_admin_jwt}"}
    response = client.delete("files/", headers=headers)
    assert response.status_code == 204
    # Validate that the file table is empty
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_all_files_004_anomalous_user_not_admin(
    monkeypatch,
    client,
    test_db_session,
    seed_jwt,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 004 - Anomalous
    Conditions: User is not an admin
    Result: HTTP 403 - Forbidden
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    headers = {"Authorization": f"Bearer {seed_jwt}"}
    response = client.delete("files/", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"
    # Validate that the file table is empty
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert len(files) == 1
    assert is_file_present("abcdefgh.jpeg")
