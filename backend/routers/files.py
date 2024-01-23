"""
routers/files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Router for dealing with file upload and download operations

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from fastapi import APIRouter, Response, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, generate_unique_id
from backend.models.models import File

router = APIRouter()


@router.get("/")
async def list_files(db: AsyncSession = Depends(get_db)):
    files = await db.execute(select(File))
    return files.scalars().all()
