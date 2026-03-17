from pydantic import BaseModel , EmailStr ,Field
from datetime import datetime
from typing import Optional ,Annotated
from pydantic.types import conint
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password : str


class userOut(BaseModel):
    id: int 
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True   

class UserLogin(BaseModel):
    email: str
    password : str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id : int 
    owner : userOut

    class Config:
        from_attributes = True

 

class Token(BaseModel):
    access_token :str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]