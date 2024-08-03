import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.database import database
from main.logging_conf import configure_logging
from main.routers.post import router as post_router

logger = logging.getLogger(__name__)
@asynccontextmanager  # Connect and disconnect from DB
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Testing logger")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router) # prefix="/posts"