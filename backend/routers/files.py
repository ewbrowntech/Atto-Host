"""
routers/files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Router for dealing with file upload and download operations

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import os
import shutil

from fastapi import APIRouter, Response, Depends, File, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, generate_unique_id
from backend.models.models import File as FileModel
from backend.get_configuration import get_config

router = APIRouter()


@router.get("/")
async def list_files(db: AsyncSession = Depends(get_db)):
    files = await db.execute(select(FileModel))
    files = files.scalars().all()
    return files


@router.post("/")
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # Ensure a file is included in the request
    if file is None:
        raise HTTPException(
            status_code=400, detail="No file was received with the request."
        )
    # Ensure the file is of an allowed type
    config = get_config()
    if file.content_type not in config["allowed_mimetypes"]:
        raise HTTPException(status_code=400, detail="File type not allowed")

    try:
        file_id = generate_unique_id()
        extension = file.filename.split(".")[-1]
        storage_filename = file_id + "." + extension
        storage_path = os.path.normpath(os.path.join("/storage/", storage_filename))
        # Save the file to the storage directory
        with open(storage_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Save file information to the database
    new_file = FileModel(
        id=file_id,
        mimetype=file.content_type,
        filename=storage_filename,
        original_filename=file.filename,
        size=file.size,
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {"id": file_id}
