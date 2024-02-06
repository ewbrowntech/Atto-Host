"""
tests/test_upload_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the uploading a file in POST files/

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import mimetypes
import os
import pytest
from sqlalchemy import select
from backend.packages.storage_driver.is_file_present import is_file_present
from backend.test.conftest import TEST_CONTENT, TEST_STORAGE, CONFIGS
from backend.models.models import File


@pytest.mark.asyncio
async def test_upload_file_000_nominal(
    monkeypatch, client, test_db_session, clear_storage_directory
):
    """
    Test 000 - Nominal
    Conditions: File of valid type included in request
    Result: File object returned
    """
    # Get the file to be uploaded
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    with open(os.path.join(TEST_CONTENT, "test_file1.jpeg"), "rb") as file:
        response = client.post(
            "files/", files={"file": ("test_file1.jpeg", file, "image/jpeg")}
        )

    assert response.status_code == 201
    assert response.json()["original_filename"] == "test_file1.jpeg"

    # Make sure the file metadata is present within the database
    query = select(File).where(File.original_filename == "test_file1.jpeg")
    result = await test_db_session.execute(query)
    file_objects = result.scalars().all()
    assert len(file_objects) == 1
    file_info = file_objects[0]
    assert file_info.mimetype == "image/jpeg"
    assert file_info.size == 430061
    assert is_file_present(file_info.filename)


@pytest.mark.asyncio
async def test_upload_file_001_anomalous_no_file_included(
    monkeypatch, client, test_db_session, clear_storage_directory
):
    """
    Test 001 - Anomalous
    Conditions: No file included in the request
    Result: HTTP 422
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    response = client.post("files/", files={})
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body", "file"]


@pytest.mark.asyncio
async def test_upload_file_002_anomalous_disallowed_mimetype(
    monkeypatch, client, test_db_session, clear_storage_directory
):
    """
    Test 002 - Anomalous
    Conditions: File is of a disallowed type
    Result: HTTP 422 - "File type not allowed"
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    with open(os.path.join(TEST_CONTENT, "7z.exe"), "rb") as file:
        response = client.post("files/", files={"file": ("7z.exe", file, "image/jpeg")})
    assert response.status_code == 422
    print(response.json()["detail"])
    assert response.json()["detail"] == "File type application/x-dosexec not allowed"


@pytest.mark.asyncio
async def test_upload_file_003_anomalous_disallowed_extension(monkeypatch, client, clear_storage_directory):
    """
    Test 003 - Anomalous
    Conditions: File is of a disallowed type
    Result: HTTP 422 - "File type not allowed
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    with open(os.path.join(TEST_CONTENT, "test_script.bat"), "rb") as file:
        response = client.post(
            "files/", files={"file": ("test_script.bat", file, "image/jpeg")}
        )
    assert response.status_code == 422
    print(response.json()["detail"])
    assert response.json()["detail"] == "File type .bat not allowed"


@pytest.mark.asyncio
async def test_upload_file_004_anomalous_oversized_file(monkeypatch, client, clear_storage_directory):
    """
    Test 004 - Anomalous
    Conditions: File size is over the allowed size
    Result: HTTP 422 - "File size is 430061B, which exceeds the maximum allowed size of 100B"
    """
    monkeypatch.setenv(
        "CONFIG_PATH", os.path.join(CONFIGS, "config_low_filesize_limit.json")
    )
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    with open(os.path.join(TEST_CONTENT, "test_file1.jpeg"), "rb") as file:
        response = client.post(
            "files/", files={"file": ("test_file1.jpeg", file, "image/jpeg")}
        )
    assert response.status_code == 422
    print(response.json()["detail"])
    assert (
        response.json()["detail"]
        == "File size is 430061B, which exceeds the maximum allowed size of 1000B"
    )
