"""
get_orphaned_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get all of the oprhaned files (files in storage without metadata in DB)

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import os
from sqlalchemy import select
from backend.models.models import File as FileModel
from backend.packages.storage_driver.get_storage_directory import get_storage_directory


async def get_orphaned_files(db):
    files = await db.execute(select(FileModel))
    files = files.scalars().all()
    filenames_in_database = [file.filename for file in files]
    filenames_in_storage = [
        filename
        for filename in os.listdir(get_storage_directory())
        if os.path.isfile(os.path.join(get_storage_directory(), filename))
        and filename != ".gitignore"
    ]
    orphaned_files = [
        filename
        for filename in filenames_in_storage
        if filename not in filenames_in_database
    ]
    return orphaned_files
