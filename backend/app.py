"""
app.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Run FastAPI application

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

from fastapi import FastAPI

from backend.database import create_tables

# Import routers
from backend.routers.files import router as files_router

app = FastAPI()
app.include_router(files_router, prefix="/files")


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}