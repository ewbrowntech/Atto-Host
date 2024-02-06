"""
models/models.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Model representing files in the database

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import func
from backend.database import Base
from sqlalchemy.orm import relationship


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class File(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, index=True)
    owner_username = Column(Integer, ForeignKey("users.username"))
    original_filename = Column(String, nullable=False, index=True)
    filename = Column(String, nullable=False, index=True)
    mimetype = Column(String, nullable=False, index=True)
    size = Column(Integer, nullable=False, index=True)
    upload_datetime = Column(DateTime, server_default=func.now())
    lifetime = Column(Integer, nullable=False, index=True, default=3600)
    owner = relationship("User", back_populates="files")


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    hashed_token = Column(String, default=None)
    files = relationship("File", back_populates="owner")
