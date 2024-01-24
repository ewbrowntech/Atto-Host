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
from backend.database import engine, Base, create_tables, drop_tables


# Fixture for setting up and tearing down the database
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session():
    await create_tables()
    yield "A"
    # Teardown (reset database)
    # await drop_tables()
