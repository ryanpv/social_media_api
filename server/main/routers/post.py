from fastapi import APIRouter, HTTPException
from main.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

@router.get("/")
async def root():
  return { "message": "Hello, world!" }

post_table = {}
comment_table = {}


def find_post(post_id: int):
  return post_table.get(post_id)


# Create post
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
  data = post.dict()
  last_record_id = len(post_table)
  print('last id', last_record_id)
  new_post = { **data, "id": last_record_id }
  post_table[last_record_id] = new_post
  return new_post


# Get all posts
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
  return list(post_table.values())


# Create comment for existing post
@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
  post = find_post(comment.post_id)
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  
  data = comment.dict()
  last_record_id = len(comment_table)
  print('last id', last_record_id)
  new_comment = { **data, "id": last_record_id }
  comment_table[last_record_id] = new_comment
  return new_comment


# Get ALL comments under post
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


# Get post with its comments
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": await get_comments_on_post(post_id)}