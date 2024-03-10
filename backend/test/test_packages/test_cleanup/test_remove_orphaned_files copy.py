"""
test_remove_orphaned_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of remove_orphaned_files()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import pytest
from app.packages.storage_driver.is_file_present import is_file_present
from app.packages.cleanup.remove_orphaned_files import remove_orphaned_files
from test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_remove_orphaned_files_000_one_orphaned_file(
    monkeypatch, test_db_session, seed_file_binary, clear_storage_directory
):
    """
    Test 000 - Nominal
    Conditions: One orphaned file
    Result: File removed
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    assert is_file_present("abcdefgh.jpeg")
    await remove_orphaned_files(test_db_session)
    assert not is_file_present("abcdefgh.jpeg")
