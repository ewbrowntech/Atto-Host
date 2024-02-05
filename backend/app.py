"""
app.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Run FastAPI application

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.database import create_tables, engine
from backend.packages.cleanup.cleanup import cleanup
from backend.limiter import limiter

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

# Import routers
from backend.routers.files import router as files_router
from backend.routers.users import router as users_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await cleanup_scheduler()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(files_router, prefix="/files")
app.include_router(users_router, prefix="/users")

# This is necessary to handle Rate Limit Exceeded error properly.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Scheduler which runs the cleanup job at a given interval
async def cleanup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cleanup, IntervalTrigger(minutes=5))
    scheduler.start()
