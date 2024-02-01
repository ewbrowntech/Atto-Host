"""
tests/test_remove_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for removing files in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import pytest
from backend.test.conftest import TEST_STORAGE


@pytest.mark.asyncio
async def test_remove_file_000_nominal_file_present(
    monkeypatch, client, seed_file_object, seed_file_binary, clear_storage_directory
):
    """
    Test 000 - Nominal
    Conditions: File object present and file present in storage
    Result: HTTP 204 - No content
    """
    # Make the request the the test client
    response = client.delete("files/abcdefgh")
    assert response.status_code == 204
