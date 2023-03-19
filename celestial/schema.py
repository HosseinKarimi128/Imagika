import re
from typing import Any, Generic, List, Optional, Type, Union, Dict
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,validator
from fastapi import UploadFile

'''
User Schemas ----------------------------------------------------------------------------------------------------
'''
class UserInSignUp(BaseModel):
    device_id: str
    email: str
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', v):
            raise ValueError('Invalid email address')
        return v

class UserInLogin(BaseModel):
    device_id: str
    
class UserOutLogin(BaseModel):
    device_id: int
    shown_name: str
    token: str
    refresh_token: str

class UserProfileOut(BaseModel):
    device_id: int
    shown_name: str
    posts: Optional[Dict]
    interacts: Optional[Dict]

class UserInInteract(BaseModel):
    post_id: int
    isLike: bool

class UserInCreatePost(BaseModel):
    user_id: int
    shown_name: str
    prompt: str
    n_prompt: str
    image_id: UUID
    topic: str

class AdminInCreateTopic(BaseModel):
    title: str
    starts_on: datetime


'''
Post Schemas -----------------------------------------------------------------------------------------------------
''' 
class PostOut(BaseModel):
    id: int
    shown_name: str
    draft: bool
    images: List[UUID]

class PostForInteract(BaseModel):
    id: int
    isLike: bool

class PostForDaVinchi(BaseModel):
    prompt: str
    n_prompt: Optional[str]
    image: UUID

class PostFromDaVinchi(BaseModel):
    images: List[UUID]

class PostForPublish(BaseModel):
    id: int
    image_number: int

class TimelineOut(BaseModel):
    queue: Optional[List[PostOut]]



'''
Topic Schemas -----------------------------------------------------------------------------------------------------
''' 

class TopicOut(BaseModel):
    id: int
    title: str

class TopicOutList(BaseModel):
    items: List[TopicOut]
    
class TopicOutInCreate(BaseModel):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
