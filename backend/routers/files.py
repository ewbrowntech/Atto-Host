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

import magic

from fastapi import APIRouter, Response, Depends, File, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, generate_unique_id
from backend.models.models import File as FileModel
from backend.get_configuration import get_config

from backend.packages.storage_driver.is_file_present import is_file_present
from backend.packages.storage_driver.get_storage_directory import get_storage_directory

router = APIRouter()


@router.get("/")
async def list_files(db: AsyncSession = Depends(get_db)):
    files = await db.execute(select(FileModel))
    files = files.scalars().all()

    return [
        {
            "id": file.id,
            "original_filename": file.original_filename,
            "filename": file.filename,
            "mimetype": file.mimetype,
            "size": file.size,
            "upload_datetime": file.upload_datetime,
            "is_file_available": is_file_present(file.filename),
        }
        for file in files
    ]


@router.post("/")
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # Ensure a file is included in the request
    if file is None:
        raise HTTPException(
            status_code=400, detail="No file was received with the request"
        )
    # Ensure the file is of an allowed type
    config = get_config()

    # Do not allow filenames with no extension
    split_filename = file.filename.split(".")
    if len(split_filename) == 1:
        raise HTTPException(status_code=422, detail=f"File type not allowed")
    else:
        file_extension = split_filename[-1]

    # Filter out disallowed mimetypes via Magic
    mime = magic.Magic(mime=True)
    content = await file.read(2048)
    await file.seek(0)
    file_type = mime.from_buffer(content)
    if file_type not in config["allowed_mimetypes"]:
        raise HTTPException(
            status_code=422, detail=f"File type {file_type} not allowed"
        )

    # Filter out disallowed file extensions
    if file_extension not in config["allowed_extensions"]:
        raise HTTPException(
            status_code=422, detail=f"File type .{file_extension} not allowed"
        )

    # Filter out files which exceed the size limit
    if file.size > config["filesize_limit"]:
        raise HTTPException(
            status_code=422,
            detail=f"File size is {file.size}B, which exceeds the maximum allowed size of {config['filesize_limit']}B",
        )

    try:
        file_id = generate_unique_id()
        extension = file.filename.split(".")[-1]
        storage_filename = file_id + "." + extension
        storage_path = os.path.normpath(
            os.path.join(get_storage_directory(), storage_filename)
        )
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

    return {
        "id": new_file.id,
        "mimetype": new_file.mimetype,
        "filename": new_file.filename,
        "original_filename": new_file.original_filename,
        "size": new_file.size,
    }


@router.get("/{file_id}")
async def view_file(file_id: str, db: AsyncSession = Depends(get_db)):
    file = await db.get(FileModel, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_response = {
        "id": file.id,
        "original_filename": file.original_filename,
        "filename": file.filename,
        "mimetype": file.mimetype,
        "size": file.size,
        "upload_datetime": file.upload_datetime,
        "is_file_available": is_file_present(file.filename),
    }
    return file_response
