"""
remove_expired_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Cleanup expired files

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from datetime import datetime
from sqlalchemy import select
from app.models.models import File as FileModel
from app.packages.storage_driver.delete_file import delete_file
from app.packages.storage_driver.is_file_present import is_file_present


async def remove_expired_files(db):
    files = await db.execute(select(FileModel))
    files = files.scalars().all()
    # Assemble a list of the ID's of the expired files removed
    expired_files_removed = []
    for file in files:
        # File's with a lifetime of 0 should not be subject to cleanup
        if file.lifetime <= 0:
            continue

        # Calculate the file's age
        file_age = datetime.now() - file.upload_datetime

        # Check if the file's age exceeds its lifetime
        if file_age.total_seconds() > file.lifetime:
            try:
                await db.delete(file)
                expired_files_removed.append(
                    {
                        "id": file.id,
                        "original_filename": file.original_filename,
                        "mimeype": file.mimetype,
                        "size": file.size,
                        "upload_datetime": file.upload_datetime,
                        "lifetime": file.lifetime,
                    }
                )
                if is_file_present(file.filename):
                    delete_file(file.filename)
            except Exception as e:
                print(f"Error deleting file {file.filename}: {str(e)}")

    await db.commit()
    return expired_files_removed
