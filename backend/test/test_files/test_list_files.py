"""
tests/test_list_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the files router in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import os
import json
import shutil
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from backend.app import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables
from backend.models.models import File as FileModel
from backend.test.conftest import TEST_CONTENT, TEST_STORAGE


@pytest.mark.asyncio
async def test_list_files_000_nominal_no_files_present(client):
    """
    Test 000 - Nominal
    Conditions: no files present
    Result: response is empty list
    """
    response = client.get("files/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_files_001_nominal_file_in_db_and_storage(
    monkeypatch,
    client,
    test_db_session,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 001 - Nominal
    Conditions: files present
    Result: [{"fileAvailable": true}]
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/")

    # Validate that the metadata is present in the database
    assert response.status_code == 200
    response_objects = response.json()
    assert len(response_objects) == 1
    file_object = response_objects[0]
    assert file_object["id"] == "abcdefgh"
    assert file_object["mimetype"] == "image/jpeg"
    assert file_object["filename"] == "abcdefgh.jpeg"
    assert file_object["original_filename"] == "test_file1.jpeg"
    assert file_object["size"] == 430061

    # Validate that the file is present in the storage directory
    assert file_object["is_file_available"] == True


@pytest.mark.asyncio
async def test_list_files_002_anomalous_file_in_db_and_not_in_storage(
    monkeypatch,
    client,
    test_db_session,
    clear_storage_directory,
):
    """
    Test 002 - Anomalous
    Conditions: file is present in database but not in storage
    Result: [{"fileAvailable": false}]
    """
    # Seed file object to test database
    file_object = FileModel(
        id="abcdefgh",
        mimetype="image/jpeg",
        filename="abcdefgh.jpeg",
        original_filename="test_file1.jpeg",
        size=430061,
    )
    test_db_session.add(file_object)
    await test_db_session.commit()

    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/")

    # Validate that the metadata is present in the database
    assert response.status_code == 200
    response_objects = response.json()
    assert len(response_objects) == 1
    file_object = response_objects[0]
    assert file_object["id"] == "abcdefgh"
    assert file_object["mimetype"] == "image/jpeg"
    assert file_object["filename"] == "abcdefgh.jpeg"
    assert file_object["original_filename"] == "test_file1.jpeg"
    assert file_object["size"] == 430061

    # Validate that the file is not present in the storage directory
    assert file_object["is_file_available"] == False


@pytest.mark.asyncio
async def test_list_files_003_anomalous_file_not_in_db_and_in_storage(
    monkeypatch, client
):
    """
    Test 003 - Anomalous
    Conditions: file present in storage but not in database
    Result: []
    """
    # Seed the file to the storage directory
    shutil.copy(
        os.path.join(TEST_CONTENT, "test_file1.jpeg"),
        os.path.join(TEST_STORAGE, "abcdefgh.jpeg"),
    )

    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/")
    assert response.status_code == 200
    assert response.json() == []
