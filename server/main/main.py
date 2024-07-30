import sys

from fastapi import FastAPI

from main.routers.post import router as post_router

app = FastAPI()

print("version:", sys.version)
print("executable", sys.executable)
app.include_router(post_router) # prefix="/posts"