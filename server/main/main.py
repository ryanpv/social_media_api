from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.database import database
from main.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router) # prefix="/posts"