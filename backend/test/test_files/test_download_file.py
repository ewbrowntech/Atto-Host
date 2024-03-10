"""
tests/test_download_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for GET files/<file_id>/download

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
import re
from app.models.models import File as FileModel
from test.conftest import TEST_CONTENT, TEST_STORAGE, TEST_DOWNLOADS


@pytest.mark.asyncio
async def test_download_file_000_nominal_public_file(
    monkeypatch,
    client,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
    clear_downloads_directory,
):
    """
    Test 000 - Nominal
    Conditions: 4 requests made, exceeding limit of 3 requests per minute
    Result: HTTP 200 | File returned
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh/download")
    assert response.status_code == 200
    print(response.content)
    assert len(response.content) == 430061

    # Validate that the filename is "test_file1.jpeg"
    content_disposition = response.headers.get("Content-Disposition")
    assert content_disposition is not None, "Content-Disposition header is missing."
    filename = re.findall('filename="(.+)"', content_disposition)
    assert filename
    filename = filename[0]
    assert filename == "test_file1.jpeg"


@pytest.mark.asyncio
async def test_download_file_001_anomalous_nonexistent_file(
    monkeypatch,
    client,
    seed_file_binary,
    clear_storage_directory,
    clear_downloads_directory,
):
    """
    Test 001 - Anomalous
    Conditions: File object in database but file itself not in storage
    Result: HTTP 404 - File not found
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh/download")
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"


@pytest.mark.asyncio
async def test_download_file_002_anomalous_file_missing_in_storage(
    monkeypatch,
    client,
    seed_file_object,
    clear_storage_directory,
    clear_downloads_directory,
):
    """
    Test 002 - File object in database but file itself not in storage
    Conditions: 4 requests made, exceeding limit of 3 requests per minute
    Result: HTTP 404 - The requested file metadata exists, but the file binary was not found in storage
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.get("files/abcdefgh/download")
    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "The requested file metadata exists, but the file binary was not found in storage"
    )


@pytest.mark.asyncio
async def test_download_file_003_anomalous_exceeded_rate_limit(client):
    """
    Test 003 - Anomalous
    Conditions: 4 requests made, exceeding limit of 3 requests per minute
    Result: HTTP 429 - Too many requests
    """
    response = client.get("files/abcdefgh/download")
    response = client.get("files/abcdefgh/download")
    response = client.get("files/abcdefgh/download")
    response = client.get("files/abcdefgh/download")
    assert response.status_code == 429
