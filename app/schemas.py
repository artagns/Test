from pydantic import BaseModel, EmailStr, ConfigDict

from typing import Optional, List

import datetime

class User(BaseModel) :
    username:  str
    email:  EmailStr
    password: str

class GetUser(BaseModel) :
    username:  str
    email:  EmailStr

class UserLogin(BaseModel) :
    username: str
    password: str

class TokenData(BaseModel) :
    username: str



class Post(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    post_id: int
    title: str
    content: str
    publish_date: datetime.datetime
    owner_username: str

class PostLike(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    post: Post  # pydantic Post
    likes: int




class PostReceive(BaseModel):
    title: Optional[str]=None
    content: Optional[str]=None
    publish_date: Optional[datetime.datetime]=None



class Like(BaseModel) :
    username: str
    post_id: int
