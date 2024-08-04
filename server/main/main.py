import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

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


app.include_router(post_router)  # prefix="/posts"


@app.exception_handler(HTTPException)  # track logs for HTTPException
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)