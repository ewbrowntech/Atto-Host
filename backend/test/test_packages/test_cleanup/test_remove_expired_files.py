"""
test_remove_expired_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of remove_expired_files()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from sqlalchemy import select
from app.models.models import File as FileModel
from datetime import datetime, timedelta
from app.packages.storage_driver.is_file_present import is_file_present
from app.packages.cleanup.remove_expired_files import remove_expired_files
from test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_remove_expired_files_000_nominal_no_expired_files_in_database(
    monkeypatch,
    client,
    test_db_session,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 000 - Nominal
    Conditions: There is a file present in the database, but it is not expired
    Result: Nothing happens
    """
    # Use the default seeded file object, which is not expired
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    expired_file_removed = await remove_expired_files(test_db_session)
    assert len(expired_file_removed) == 0

    # Get the list of file metadata
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    file = files[0]
    # Validate that the file metadata was not deleted from the database
    assert file.id == "abcdefgh"
    # Validate that athe file was not removed from storage
    assert is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_expired_files_001_nominal_expired_file_in_db_and_storage(
    monkeypatch,
    client,
    test_db_session,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 001 - Nominal
    Conditions: There is an expired file present in the database
    Result: Expired file is removed from database and storage
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    # Seed expired file object to test database
    file_object = FileModel(
        id="abcdefgh",
        mimetype="image/jpeg",
        filename="abcdefgh.jpeg",
        original_filename="test_file1.jpeg",
        size=430061,
        upload_datetime=datetime.now() - timedelta(hours=1),
    )
    test_db_session.add(file_object)
    await test_db_session.commit()
    expired_file_removed = await remove_expired_files(test_db_session)

    assert len(expired_file_removed) == 1
    assert expired_file_removed[0]["id"] == "abcdefgh"
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")


@pytest.mark.asyncio
async def test_remove_expired_files_002_anomalous_expired_file_in_db_and_not_storage(
    monkeypatch,
    test_db_session,
    clear_storage_directory,
):
    """
    Test 002 - Anomalous
    Conditions: There is an expired file present in the database, but its file is missing in storage
    Result: Expired file metadata is removed from database
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    # Seed expired file object to test database
    file_object = FileModel(
        id="abcdefgh",
        mimetype="image/jpeg",
        filename="abcdefgh.jpeg",
        original_filename="test_file1.jpeg",
        size=430061,
        upload_datetime=datetime.now() - timedelta(hours=1),
    )
    test_db_session.add(file_object)
    await test_db_session.commit()
    expired_file_removed = await remove_expired_files(test_db_session)

    assert len(expired_file_removed) == 1
    assert expired_file_removed[0]["id"] == "abcdefgh"
    files = await test_db_session.execute(select(FileModel))
    files = files.scalars().all()
    assert files == []
    assert not is_file_present("abcdefgh.jpeg")
