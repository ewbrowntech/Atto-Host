"""
routers/users.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Router for user registration and login

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.models import User
from backend.schema.user import UserSchema

router = APIRouter()

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(user_input: UserSchema, db: AsyncSession = Depends(get_db)):
    # Check if a user already exists
    result = await db.execute(select(User).filter(User.username == user_input.username))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail=f"Username is already taken")

    # If the username does not already exist, create a user object
    hashed_password = pwd_context.hash(user_input.password)
    user = User(username=user_input.username, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Return the username
    return f"User {user.username} created."
