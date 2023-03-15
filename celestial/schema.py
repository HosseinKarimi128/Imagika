import re
from typing import Any, Generic, List, Optional, Type, Union, Dict
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,validator
from fastapi import UploadFile

'''
User Schemas ----------------------------------------------------------------------------------------------------
'''
    
class BaseUser(BaseModel):
    device_id: str

class UserRegister(BaseUser):
    email: str
    # @validator('device_id')
    # def validate_device_id(cls, v):
    #     if not re.match(r'^[A-Fa-f0-9]{8}$', v):
    #         raise ValueError('Invalid device ID')
    #     return v
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', v):
            raise ValueError('Invalid email address')
        return v
    
class UserLoginOut(BaseUser):
    access_token: str
    refresh_token: str
    shown_name: str
    queue: Optional[Dict]
'''
Post Schemas -----------------------------------------------------------------------------------------------------
''' 

class PostBase(BaseModel):
    user: int
    title: str
    class Config:
        orm_mode = True

class CreatePost(BaseModel):
    topic: int
    prompt: str
    n_prompt: Optional[str] = None
    uploaded_image: Optional[UUID] = None

class CreatePostOut(CreatePost):
    id = int

class UpdatePost(PostBase):
    view_count: int
    activPoste: bool

class SinglePost(PostBase):
    id: int

class AllPostList(PostBase):
    id: int
    slug: str
    draft: bool = False

class ImagePost(BaseModel):
    file_id: UUID
    post_id: int
    gnerated: bool

class IntractPost(BaseModel):
    post_id: int
    isLike: bool

class IntractOut(BaseModel):
    post_id: int
    liked_count: int
    disliked_count: int
    score: int


'''
File Schemas -----------------------------------------------------------------------------------------------------
''' 

class FileBase(BaseModel):
    name = str
    class Config:
        orm_mode = True

class FileOut(FileBase):
    guid: UUID
    path: str
    class Config:
        orm_mode = True

class FileForRespose(BaseModel):
    post_id: UUID

class FileInResponse(BaseModel):
    guid: UUID


'''
Topic Schemas -----------------------------------------------------------------------------------------------------
''' 

class TopicInCreate(BaseModel):
    title: str

class TopicsInResponce(BaseModel):
    titles: List[str]

'''
Queue Schemas -----------------------------------------------------------------------------------------------------
''' 

class QueueItem(BaseModel):
    device_id: int
    shown_name: str
    post_id: int
    image: Optional[str]

class QueueOut(BaseModel):
    count: int
    queue: List[QueueItem]