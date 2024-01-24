"""
tests/test_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality for the files router in routers/files.py

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from backend.app import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base, create_tables, drop_tables

client = TestClient(app)


@pytest.mark.asyncio
async def test_read_main():
    response = client.get("files/")
    assert response.status_code == 200
    assert response.json() == []
