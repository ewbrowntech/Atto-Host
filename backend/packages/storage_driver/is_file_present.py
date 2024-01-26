"""
storage_driver/is_file_present.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Check to see if a file is present in the storage directory

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import os


def is_file_present(filename: str):
    filepath = os.path.join(os.environ.get("STORAGE_PATH"), filename)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return True
    else:
        return False
