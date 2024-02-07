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

from fastapi import (
    APIRouter,
    Request,
    Response,
    Depends,
    File,
    UploadFile,
    HTTPException,
)
from fastapi.responses import FileResponse
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.limiter import limiter

from backend.database import get_db, generate_unique_id
from backend.models.models import File as FileModel
from backend.models.models import User

from backend.get_configuration import get_config

from backend.packages.storage_driver.is_file_present import is_file_present
from backend.packages.storage_driver.get_storage_directory import get_storage_directory
from backend.packages.storage_driver.delete_file import delete_file
from backend.packages.tokens.get_current_user import get_current_user

router = APIRouter()


@router.get("/", status_code=200)
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


@router.post("/", status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
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

    # Save the file to the user's files
    stmt = (
        select(User).options(selectinload(User.files)).filter_by(username=user.username)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    user.files.append(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {
        "id": new_file.id,
        "mimetype": new_file.mimetype,
        "filename": new_file.filename,
        "original_filename": new_file.original_filename,
        "size": new_file.size,
    }


@router.delete("/", status_code=204)
async def remove_all_files(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    try:
        # Validate that the file object has been deleted
        await db.execute(delete(FileModel))
        await db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Remove the files in the storage directory
    for filename in os.listdir(get_storage_directory()):
        filepath = os.path.join(get_storage_directory(), filename)
        # TODO: Could run into an issue here where one of the files fails to delete.
        # This would result in the files becoming orphaned. Think of a better solution later
        if filename != ".gitignore":
            os.remove(filepath)


@router.get("/{file_id}", status_code=200)
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


@router.delete("/{file_id}", status_code=204)
async def remove_file(
    file_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Remove a file by its ID
    """
    file = await db.get(FileModel, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    try:
        delete_file(file.filename)
    except FileNotFoundError:
        pass
    await db.delete(file)
    await db.commit()
    return Response(status_code=204)


@router.get("/{file_id}/download", status_code=200)
@limiter.limit("3/minute")
async def download_file(
    request: Request,
    file_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Download a file binary by its ID
    """
    file = await db.get(FileModel, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if not is_file_present(file.filename):
        raise HTTPException(
            status_code=404,
            detail="The requested file metadata exists, but the file binary was not found in storage",
        )
    return FileResponse(
        path=os.path.join(get_storage_directory(), file.filename),
        filename=file.original_filename,
    )
