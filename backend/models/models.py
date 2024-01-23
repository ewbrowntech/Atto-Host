"""
models/models.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Model representing files in the database

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncEngine

Base = declarative_base()


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class File(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, index=True)
