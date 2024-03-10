"""
storage_driver/delete_file.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Remove a file from the storage directory

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import os
from app.packages.storage_driver.is_file_present import is_file_present
from app.packages.storage_driver.get_storage_directory import get_storage_directory


def delete_file(filename: str):
    if not is_file_present(filename):
        raise FileNotFoundError
    filepath = os.path.join(get_storage_directory(), filename)
    try:
        os.remove(filepath)
    except Exception as e:
        raise FileDeletionException(filename, e)
    if os.path.exists(filepath):
        raise FileDeletionException(filename)


class FileDeletionException(Exception):
    """Exception raise when a file deletion operation fails"""

    def __init__(self, filename, exception=None):
        self.message = f"Failed to delete file {filename}"
        if exception is not None:
            self.message += ". Encounted the following exception:\n{exception}"
        super().__init__(self.message)
