"""
schema/user.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Schema representing a user

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
