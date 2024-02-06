"""
tokens/get_current_user.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the current user from a JWT. 

This file is based on the example provided in FastAPI's documentation.
The original can be found here: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ 

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.database import get_db
from backend.models.models import User
from backend.packages.tokens.get_secret_key import get_secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def credentials_exception(
    detail: str = "Could not validate credentials",
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(db, token: str = Depends(oauth2_scheme)):
    if token is None:
        raise credentials_exception(detail="No JWT included in request")
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception("JWT did not include a username")
    except JWTError:
        raise credentials_exception(detail="JWT could not be decoded")
    user = await db.get(User, username)
    if user is None:
        raise credentials_exception(detail="User specified by JWT does not exist")
    return user
