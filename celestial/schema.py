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
    device_id: str
    shown_name: str
    posts: Optional[Dict]
    token: str
    refresh_token: str
    magic: Optional[int]

class UserProfileOut(BaseModel):
    device_id: str
    shown_name: str
    posts: Optional[Dict]
    interacts: Optional[Dict]
    magic: Optional[int]

class UserInInteract(BaseModel):
    post_id: int
    isLike: bool

class UserInCreatePost(BaseModel):
    user_device_id: str
    shown_name: str
    prompt: str
    n_prompt: str
    image_id: str
    topic_id: int

class AdminInCreateTopic(BaseModel):
    title: str
    description: str
    starts_on: datetime


'''
Post Schemas -----------------------------------------------------------------------------------------------------
''' 
class PostOut(BaseModel):
    id: int
    shown_name: str
    images: Dict

class PostForInteract(BaseModel):
    id: int
    isLike: bool

class PostForDaVinchi(BaseModel):
    prompt: str
    n_prompt: Optional[str]
    image: str

class PostFromDaVinchi(BaseModel):
    images: Dict

class PostForPublish(BaseModel):
    id: int
    image_number: int

class PostPublishOut(BaseModel):
    id: int
    shown_name: str
    image: str

class TimelineOut(BaseModel):
    queue: Optional[List]



'''
Topic Schemas -----------------------------------------------------------------------------------------------------
''' 

class TopicOut(BaseModel):
    id: int
    title: str
    description: str

class TopicOutList(BaseModel):
    items: List[TopicOut]
    
class TopicOutInCreate(BaseModel):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
