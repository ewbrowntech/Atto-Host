"""
test_storage_driver.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for storage check in packages/storage_driver

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import os
import shutil
import pytest
from app.packages.storage_driver.is_file_present import is_file_present
from app.packages.storage_driver.get_storage_directory import get_storage_directory
from test.conftest import TEST_CONTENT, TEST_STORAGE


def test_get_storage_directory_000_nominal_valid_storage_directory(monkeypatch):
    """
    Test 000 - Nominal
    Conditions: valid storage directory set
    Resul: storage directory returned
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    assert get_storage_directory() == TEST_STORAGE


def test_get_storage_directory_001_anomalous_storage_directory_not_set():
    """
    Test 001 - Anomalous
    Conditions: environment variable "STORAGE_DIRECTORY" is not set
    Resul: EnvironmentError("The environment variable 'STORAGE_DIRECTORY' is not set")
    """
    with pytest.raises(EnvironmentError) as e:
        storage_directory = get_storage_directory()
    assert str(e.value) == "The environment variable 'STORAGE_DIRECTORY' is not set"


def test_get_storage_directory_002_anomalous_storage_directory_does_not_exist(
    monkeypatch,
):
    """
    Test 002 - Anomalous
    Conditions: environment variable "STORAGE_DIRECTORY" is set but does not exist
    Resul: FileNotFoundException("The path representent by environment variable 'STORAGE_DIRECTORY' does not exist")
    """
    monkeypatch.setenv("STORAGE_PATH", "Nonexistent/Path")
    with pytest.raises(FileNotFoundError) as e:
        storage_directory = get_storage_directory()
    assert (
        str(e.value)
        == "The path representent by environment variable 'STORAGE_DIRECTORY' does not exist"
    )


def test_get_storage_directory_003_anomalous_storage_directory_is_not_dir(
    monkeypatch,
):
    """
    Test 003 - Anomalous
    Conditions: environment variable "STORAGE_DIRECTORY" is set and exists, but is not a directory
    Resul:  NotADirectoryError("The environment variable 'STORAGE_DIRECTORY' does not represent a directory")
    """
    monkeypatch.setenv("STORAGE_PATH", os.path.join(TEST_CONTENT, "test_file1.jpeg"))
    with pytest.raises(NotADirectoryError) as e:
        storage_directory = get_storage_directory()
    assert (
        str(e.value)
        == "The environment variable 'STORAGE_DIRECTORY' does not represent a directory"
    )


def test_is_file_present_000_file_present(
    monkeypatch, seed_storage_directory, clear_storage_directory
):
    """
    Test 000 - Nominal
    Conditions: no files present
    Result: response is empty list
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    assert is_file_present("test_file1.jpeg")


def test_is_file_present_001_file_not_present(monkeypatch):
    """
    Test 001 - Nominal
    Conditions: no files present
    Result: response is empty list
    """
    monkeypatch.setenv("STORAGE_PATH", TEST_STORAGE)
    assert not is_file_present("test_file1.jpeg")
