"""
conftest.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up an isolated, in-memory database for tests

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables, get_db
from backend.app import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


# Fixture for creating
@pytest_asyncio.fixture(scope="function")
async def test_db():
    # Set up the test database
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Replace with your metadata

    # Create a new session for each test
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session  # use this session in tests

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db):
    # Override the app's dependency to use the test database
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    # Replace 'myapp.dependencies.get_db' with your actual dependency

    from fastapi.testclient import TestClient

    client = TestClient(app)
    yield client


# Fixture for setting up and tearing down the database
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session():
    await create_tables()
    yield
    await drop_tables()
