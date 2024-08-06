import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from main.database import comment_table, database, like_table, post_table
from main.models.post import (
    Comment,
    CommentIn,
    PostLike,
    PostLikeIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)
from main.models.user import User
from main.security import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def root():
  return { "message": "Hello, world!" }


async def find_post(post_id: int):
    logger.info(f"Finding post with id: {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


# Create post
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(
    post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Creating post")

    data = {**post.dict(), "user_id": current_user.id}
    query = post_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


# Get all posts
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    logger.info("Getting all posts")
    query = post_table.select()

    logger.debug(query)

    posts = await database.fetch_all(query)

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")

    return posts


# Create comment for existing post
@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(
    comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Creating comment")

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {comment.post_id} not found"
        )

    data = {**comment.dict(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


# Get ALL comments under post
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info("Getting comments on post")

    query = comment_table.select().where(comment_table.c.post_id == post_id)

    logger.debug(query)

    post_comments = await database.fetch_all(query)
    if not post_comments:
        raise HTTPException(
            status_code=404, detail=f"No comments found under post with id: {post_id}"
        )

    return post_comments


# Get post with its comments
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    logger.info("Getting post and its comments")

    post = await find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )

    return {"post": post, "comments": await get_comments_on_post(post_id)}


@router.post("/like", response_model=PostLike, status_code=201)
async def like_post(
    like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Liking post")

    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {like.post_id} not found"
        )

    data = {**like.dict(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}