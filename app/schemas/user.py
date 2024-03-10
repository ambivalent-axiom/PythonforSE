from typing import List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(
        title="The Username",
        description="This is description of username",
        default=None,
    )
    liked_posts: Optional[List[int]] = Field(
        description="Array of post ids the user liked", default=[]
    )


class FullUserProfile(User):
    short_description: str
    long_bio: str


class MultipleUsersResponse(BaseModel):
    users: list[FullUserProfile]
    total: int


class CreateUserResponse(BaseModel):
    user_id: int
