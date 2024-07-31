from pydantic import (
  BaseModel,  # class that allows us to define model - model validates data
)


class UserPostIn(BaseModel):
  body: str


class UserPost(UserPostIn):
    id: int

    class Config:
        orm_mode = True  # for returning sql alchemy obj | dict


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int

    class Config:
        orm_mode = True


class UserPostWithComments(BaseModel):
  post: UserPost
  comments: list[Comment]