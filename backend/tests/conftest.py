"""
conftest.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up an isolated, in-memory database for tests

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


# Fixture for setting up and tearing down the database
@pytest.fixture(scope="function")
async def async_db_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Setup for a test
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session  # This is where the test runs

    # Teardown (reset database)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
