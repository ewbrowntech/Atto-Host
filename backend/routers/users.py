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

from backend.packages.tokens.generate_jwt import generate_jwt

router = APIRouter()

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=201)
async def register(user_input: UserSchema, db: AsyncSession = Depends(get_db)):
    # Check if a user already exists
    result = await db.execute(select(User).filter(User.username == user_input.username))
    if result.scalars().first() is not None:
        raise HTTPException(
            status_code=400, detail=f"Username {user_input.username} is already taken"
        )

    # If the username does not already exist, create a user object
    hashed_password = pwd_context.hash(user_input.password)
    user = User(username=user_input.username, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Return the username
    return {"detail": f"User {user.username} created"}


@router.post("/login", status_code=200)
async def login(user_input: UserSchema, db: AsyncSession = Depends(get_db)):
    # Validate the provided credentials
    user = await db.get(User, user_input.username)
    if user is None or not pwd_context.verify(
        user_input.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401, detail="The provided credentials were incorrect"
        )

    # Generate a JSON Web Token (JWT)
    jwt = generate_jwt(user_input.username)
    # Hash the JWT and store it in the user object so that the user must always the latest one generated
    user.hashed_token = pwd_context.hash(jwt)
    db.add(user)
    await db.commit()

    return jwt
