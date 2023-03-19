from http.client import HTTPResponse
from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Security
from fastapi.responses import FileResponse
from django.contrib.auth.models import User
from contlika.settings import STATIC_URL
from celestial.models import UserProfile, Post, Topic
from celestial.schema import *
from celestial.auth import Auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from celestial.services import *
import logging

#==============================================================
logger = logging.getLogger(__name__)

user = APIRouter()
post = APIRouter()
topic = APIRouter()
file = APIRouter()


_post = Post.objects

#==============================================================

security = HTTPBearer()
auth_handler = Auth()

@user.post('/signup', status_code=201, response_model = str)
async def signup(request:UserInSignUp):
    try:
        await on_signup(request)
    except Exception: 
        if user != None:
            logger.info(request.__dict__)
            logger.exception(Exception)
            raise HTTPException(status_code=409, detail='Account is already existed') 
        else:
            raise Exception
    return 'The user is created'

"""     try:
        hashed_password = auth_handler.encode_password(user_details.password)
        user = User.objects.create_user(
				username = user_details.username,
				password = hashed_password
						)
        return user
    except:
        error_msg = 'Failed to signup user'
        return error_msg """

@user.post('/login', status_code=200, response_model = UserOutLogin)
async def login(request:UserInLogin):
    response = on_user_login(request)
    if response:
        return response
    else: 
        return HTTPException(status_code=404, detail='User not Existed')

@user.get('/refresh_token', status_code=200)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = await credentials.credentials
    new_token = await auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

def user_authorizer(credentials: HTTPAuthorizationCredentials = Security(security)) -> UserProfile:
    token = credentials.credentials
    device_id = auth_handler.decode_token(token)
    try:
        return on_get_profile(device_id)
    except:
        raise HTTPException(status_code=401, detail='Unauthorized')

@user.get('/get_user', status_code=200, response_model = UserProfileOut)
async def get_user(user = Depends(user_authorizer)):
    try:
        return user
    except Exception:
        logger.info(user.__dict__)
        logger.error(Exception)
        raise HTTPException(status_code=404, detail='user not found')

@user.get('/get_timeline',status_code=200, response_model= TimelineOut)
async def get_timeline(user = Depends(user_authorizer)):
    try:
        return await on_get_timeline(user)
    except:
        logger.info(user.__dict__)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='the user queue counld not be created')

    
#-----------------------------------------------------------
@file.post("/upload_file/", status_code=201)
async def upload_file(uploaded_file: UploadFile = File(...)):
    uploaded_file.filename = str(uuid.uuid4())
    file_location = f"images/{uploaded_file.filename}.png"
    with open(file_location, "wb+") as file_object:
         file_object.write(uploaded_file.file.read())
    return uploaded_file.filename

@file.get("/{file_id}",status_code=200)
async def get_file(file_id: str, user = Depends(user_authorizer)):
    return FileResponse("images/"+file_id+'.png')


#------------------------------------------------------------
@post.get("/get_topics", satus_code = 200,response_model = TopicOutList)
async def get_topics(user = Depends(user_authorizer)):
    return await on_get_topic()

@post.post("/create/", status_code=201, response_model = PostOut)
async def create_post(request: UserInCreatePost,user = Depends(user_authorizer)):   
    try:
        return await on_create_post(request)
    except Exception:
        logger.error('the object with following data could not be created')
        logger.info(request)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='Object Cannot be created with this data')

@post.put('/intract/',status_code = 200, response_model = str)
async def post_interact(request: PostForInteract, user = Depends(user_authorizer)):
    try:
        await on_post_interact_update(user, request)
    except ObjectDoesNotExist:
        logger.info(request,user)
        logger.exception(ObjectDoesNotExist)
        raise HTTPException(status_code=404, detail="Post not found")
    except IntegrityError:
        logger.info(request,user)
        logger.exception(IntegrityError)
        logger.error('Failed to save the changes due to a conflict')
        raise HTTPException(status_code=409, detail="Conflict")
    except Exception:
        logger.info(request,user)
        logger.error(Exception)
        raise HTTPException(status_code=500, detail='There is an error with saving interactions')
    try:
        if await has_user_interacted(user, request):
            logger.info(request)
            logger.info(user.__dict__)
            raise HTTPException(status_code = 409, detail ='already interacted with this post')
    except Exception:
        logger.info(request)
        logger.info(user.__dict__)
        logger.error(Exception)
        raise HTTPException(status_code=500, detail="There is an error with loading interactions")
    return {"status": 1, "message": "Interaction recorded successfully"}

@post.delete('/delete/{post_id}/')
async def delete_post(post_id,user=Depends(user_authorizer)):
    try:
        await on_delete_post(post_id)
        return(f'Post with {post_id} id has been deleted')
    except Exception:
        logger.info(post_id,user)
        logger.error(Exception)
        raise HTTPException(status_code=404, detail='There is no post with this id')


#-----------------------------------------------------------

@topic.post("/create/", status_code=201, response_model = TopicOutInCreate)
async def create_new_topic(request: AdminInCreateTopic, user  = Depends(user_authorizer)) -> Any:
    try:
        return await on_create_topic(request)
    except Exception:
        logger.error('the object with following data could not be created')
        logger.info(request)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='Object Cannot be created with this data')

@topic.delete("/delete_topic/{topic_id}",status_code=200)
async def delete_topic(topic_id, user = Depends(user_authorizer)):
    on_delete_topic(topic_id)