from typing import Optional

from pydantic import (
  BaseModel,  # class that allows us to define model - model validates data
)


class UserPostIn(BaseModel):
  body: str


class UserPost(UserPostIn):
    id: int
    user_id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True  # for returning sql alchemy obj | dict

class UserPostWithLikes(UserPost):
    likes: int

    class Config:
        orm_mode = True


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int