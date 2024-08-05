import logging

from fastapi import APIRouter, HTTPException
from main.database import database, user_table
from main.models.user import UserIn
from main.security import get_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=400, detail="A user with this email already exists"
        )
    query = user_table.insert().values(email=user.email, password=user.password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created."}
