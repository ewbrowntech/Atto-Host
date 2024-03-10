"""
database.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Manage database operations

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import os
import secrets
from typing import cast, Type

from alembic.config import Config
from alembic import command

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./atto.db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=cast(Type[AsyncSession], AsyncSession), expire_on_commit=False
)

Base = declarative_base()


# Create the tables
async def create_tables(db_engine=engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created")


# Drop all of the tables
async def drop_tables(db_engine=engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables dropped")


def generate_unique_id():
    return secrets.token_hex(4)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # Handle or log the exception as needed
            raise
