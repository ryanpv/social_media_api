# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# This is a workaround to import the main module from the tests directory.

import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from main.database import database
from main.logging_conf import configure_logging
from main.routers.post import router as post_router
from main.routers.upload import router as upload_router
from main.routers.user import router as user_router

logger = logging.getLogger(__name__)

@asynccontextmanager  # Connect and disconnect from DB
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Testing logger")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)


app.include_router(post_router)  # prefix="/posts"
app.include_router(user_router)  # prefix="/users"
app.include_router(upload_router)  # prefix="/upload"


@app.exception_handler(HTTPException)  # track logs for HTTPException
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)