"""
test_get_orphaned_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_orphaned_files()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from backend.packages.cleanup.get_orphaned_files import get_orphaned_files
from backend.test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_get_orphaned_files_000_no_orphaned_files(
    monkeypatch,
    test_db_session,
    seed_file_object,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 000 - Nominal
    Conditions: File in db and storage
    Result: orphaned_files == []
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    orphaned_files = await get_orphaned_files(test_db_session)
    assert orphaned_files == []


@pytest.mark.asyncio
async def test_get_orphaned_files_001_one_orphaned_filed(
    monkeypatch,
    test_db_session,
    seed_file_binary,
    clear_storage_directory,
):
    """
    Test 001 - Nominal
    Conditions: File not in db, but in storage
    Result: orphaned_files == ["abcdefgh.jpeg"]
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    orphaned_files = await get_orphaned_files(test_db_session)
    assert orphaned_files == ["abcdefgh.jpeg"]
