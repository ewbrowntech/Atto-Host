"""
tests/test_view_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the files router in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_view_file_000_nominal(
    monkeypatch, client, seed_file_object, seed_file_binary, clear_storage_directory
):
    """
    Test 000 - Nominal
    Conditions: File object present and file present in storage
    Result: HTTP 200 - <{file_object}>
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh")

    # Validate the metadata
    assert response.status_code == 200
    file_object = response.json()
    assert file_object["id"] == "abcdefgh"
    assert file_object["mimetype"] == "image/jpeg"
    assert file_object["filename"] == "abcdefgh.jpeg"
    assert file_object["original_filename"] == "test_file1.jpeg"
    assert file_object["size"] == 430061

    # Validate that the file is preset in the storage directory
    assert file_object["is_file_available"] == True


@pytest.mark.asyncio
async def test_view_file_001_anomalous_nonexistent_file(
    monkeypatch, client, seed_file_binary, clear_storage_directory
):
    """
    Test 001 - Anomalous
    Conditions: File object not present in database
    Result: HTTP 404 - File not found
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh")

    # Validate the metadata
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}


@pytest.mark.asyncio
async def test_view_file_002_anomalous_file_missing_in_storage(
    monkeypatch, client, seed_file_object, clear_storage_directory
):
    """
    Test 002 - Nominal
    Conditions: File object present in database but file itself not in storage
    Result: HTTP 200 - [{"fileAvailable": false}]
    """
    # Make the request the the test client
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh")

    # Validate the metadata
    assert response.status_code == 200
    file_object = response.json()
    assert file_object["id"] == "abcdefgh"
    assert file_object["mimetype"] == "image/jpeg"
    assert file_object["filename"] == "abcdefgh.jpeg"
    assert file_object["original_filename"] == "test_file1.jpeg"
    assert file_object["size"] == 430061

    # Validate that the file is preset in the storage directory
    assert file_object["is_file_available"] == False
