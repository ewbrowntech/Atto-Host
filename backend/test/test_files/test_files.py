"""
tests/test_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the files router in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import json
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from backend.app import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables
from backend.models.models import File as FileModel


@pytest.mark.asyncio
async def test_read_main(client):
    """
    Test 000 - Nominal
    Conditions: no files present
    Result: response is empty list
    """
    response = client.get("files/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_001_view_files_files_present(
    client,
    test_db_session,
    seed_storage_directory,
    clear_storage_directory,
):
    """
    Test 000=1 - Nominal
    Conditions: files present
    Result: response is a list with one file object
    """
    print("Seeding file object to database")
    file_object = FileModel(
        id="abcdefgh",
        mimetype="image/jpeg",
        filename="abcdefgh.jpeg",
        original_filename="test_file1.jpeg",
        size=430061,
    )
    test_db_session.add(file_object)
    await test_db_session.commit()

    response = client.get("files/")
    assert response.status_code == 200
    response_objects = response.json()
    assert len(response_objects) == 1
    file_object = response_objects[0]
    assert file_object["id"] == "abcdefgh"
    assert file_object["mimetype"] == "image/jpeg"
    assert file_object["filename"] == "abcdefgh.jpeg"
    assert file_object["original_filename"] == "test_file1.jpeg"
    assert file_object["size"] == 430061
