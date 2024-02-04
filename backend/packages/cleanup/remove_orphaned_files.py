"""
remove_orphaned_files.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Cleanup orphaned files

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from backend.packages.cleanup.get_orphaned_files import get_orphaned_files
from backend.packages.storage_driver.delete_file import delete_file


async def remove_orphaned_files(db):
    orphaned_files = await get_orphaned_files(db)
    for filename in orphaned_files:
        delete_file(filename)
