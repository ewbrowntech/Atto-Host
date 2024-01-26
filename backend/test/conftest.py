"""
conftest.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up an isolated, in-memory database for tests

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import os
import shutil
import glob
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables, get_db
from backend.app import app
from backend.models.models import File as FileModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test/test.db"
TEST_STORAGE = os.path.join(os.path.dirname(__file__), "test_storage")
TEST_CONTENT = os.path.join(os.path.dirname(__file__), "test_content")


# Fixture for creating test db engine
@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    # Set up the test database
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


# Fixture for creating
@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_db_engine):
    # Create a new session for each test
    async_session = sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session  # use this session in tests


@pytest_asyncio.fixture(scope="function")
async def client(test_db_session):
    # Override the app's dependency to use the test database
    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    client = TestClient(app)
    yield client


# Fixture for seeding storage directory
@pytest_asyncio.fixture(scope="function")
async def seed_storage_directory():
    print("Seeding hosted test files")
    for filename in os.listdir(TEST_CONTENT):
        filepath = os.path.join(TEST_CONTENT, filename)
        if filename != "__init__.py" and os.path.isfile(filepath):
            shutil.copy(filepath, TEST_STORAGE)
    yield


# Fixture for tearing down storage folder
@pytest_asyncio.fixture(scope="function")
async def clear_storage_directory():
    yield
    for filename in os.listdir(TEST_STORAGE):
        filepath = os.path.join(TEST_STORAGE, filename)
        if filename != "__init__.py":
            os.remove(filepath)
    print("Removing hosted test files")


# Fixture for setting up and tearing down the database
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session(test_db_engine):
    await create_tables(test_db_engine)
    yield
    await drop_tables(test_db_engine)
