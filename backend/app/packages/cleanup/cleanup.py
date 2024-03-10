"""
cleanup.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Run cleanup script expired and orphaned files

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import logging
from app.packages.cleanup.remove_expired_files import remove_expired_files
from app.packages.cleanup.remove_orphaned_files import remove_orphaned_files
from app.database import get_db

logger = logging.getLogger(__name__)


async def cleanup():
    async for db in get_db():
        # Remove expired files
        logger.info("Commencing cleanup...")
        expired_files_removed = await remove_expired_files(db)
        filenames_removed = [
            file["original_filename"] for file in expired_files_removed
        ]
        if len(filenames_removed) == 0:
            logger.info("No expired files found")
        else:
            logger.info(f"Removed the following expired files: {filenames_removed}")

        # Remove orphaned files
        filenames_removed = await remove_orphaned_files(db)
        if len(filenames_removed) == 0:
            logger.info("No orphaned files found")
        else:
            logger.info(f"Removed the following orphaned files: {filenames_removed}")
        logger.info("Cleanup complete\n")
