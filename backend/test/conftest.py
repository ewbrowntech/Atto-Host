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
import secrets
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables, get_db
from backend.app import app
from backend.models.models import File as FileModel
from backend.models.models import User
from backend.routers.users import pwd_context
from backend.packages.tokens.generate_jwt import generate_jwt

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test/test.db"
TEST_STORAGE = os.path.join(os.path.dirname(__file__), "test_storage")
TEST_CONTENT = os.path.join(os.path.dirname(__file__), "test_content")
TEST_DOWNLOADS = os.path.join(os.path.dirname(__file__), "test_downloads")
CONFIGS = os.path.join(os.path.dirname(__file__), "configs")


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


@pytest_asyncio.fixture(scope="function")
async def seed_user(monkeypatch, test_db_session):
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("SECRET_KEY", test_secret_key)
    # Create a test user
    hashed_password = pwd_context.hash("password")
    user = User(username="test-user", hashed_password=hashed_password)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    yield user


@pytest_asyncio.fixture(scope="function")
async def seed_jwt(monkeypatch, test_db_session, seed_user):
    jwt = generate_jwt(seed_user.username)
    seed_user.hashed_token = pwd_context.hash(jwt)
    await test_db_session.commit()
    yield jwt


@pytest_asyncio.fixture(scope="function")
async def seed_file_object(test_db_session):
    # Seed file object to test database
    file_object = FileModel(
        id="abcdefgh",
        mimetype="image/jpeg",
        filename="abcdefgh.jpeg",
        original_filename="test_file1.jpeg",
        size=430061,
    )
    test_db_session.add(file_object)
    await test_db_session.commit()
    yield


@pytest_asyncio.fixture(scope="function")
async def seed_file_binary():
    # Seed the file to the storage directory
    shutil.copy(
        os.path.join(TEST_CONTENT, "test_file1.jpeg"),
        os.path.join(TEST_STORAGE, "abcdefgh.jpeg"),
    )
    yield


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
        if filename != ".gitignore":
            os.remove(filepath)
    print("Storage directory cleared")


# Fixture for tearing down downloads folder
@pytest_asyncio.fixture(scope="function")
async def clear_downloads_directory():
    yield
    for filename in os.listdir(TEST_DOWNLOADS):
        filepath = os.path.join(TEST_DOWNLOADS, filename)
        if filename != ".gitignore":
            os.remove(filepath)
    print("Downloads directory cleared")


# Fixture for setting up and tearing down the database
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session(test_db_engine):
    await create_tables(test_db_engine)
    yield
    await drop_tables(test_db_engine)
