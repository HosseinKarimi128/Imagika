from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Security
from fastapi.responses import FileResponse
from django.contrib.auth.models import User
from contlika.settings import STATIC_URL
from core.models import UserProfile, Post, Topic
from core.schema import *
from core.auth import Auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from core.services import *
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

@user.post('/signup')
async def signup(user_details:UserRegister):
    try:
        await create_user(device_id = user_details.device_id, email = user_details.email)
    except Exception: 
        if user != None:
            return 'Account already exists'
        else:
            raise Exception
    return {'device_id': user_details.device_id} 

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

@user.post('/login')
async def login(user_details:BaseUser):
    try: 
        user = await get_user_by_username_async(user_details.device_id)
    except: return 'User not Exist'
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid Device')
    # if (not auth_handler.verify_password(user_details.password, user.password)):
    #     return HTTPException(status_code=401, detail='Invalid password')
    shown_name = user.first_name
    # queue = _user_profile.get(id=user.id).get_queue()
    access_token = auth_handler.encode_token(user.username)
    refresh_token = auth_handler.encode_refresh_token(user.username)
    # return {'access_token': access_token, 'refresh_token': refresh_token}
    return UserLoginOut(access_token = access_token, refresh_token= refresh_token,
                         shown_name= shown_name, device_id = user_details.device_id
                         )

@user.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = await credentials.credentials
    new_token = await auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

def user_authorizer(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    username = auth_handler.decode_token(token)
    try:
        return get_user_by_username(username)
    except:
        raise HTTPException(status_code=400, detail='Invalid Device')

@user.get('/get_user')
async def get_user(user = Depends(user_authorizer)):
    try:
        return user.__dict__
    except Exception:
        logger.info(user.__dict__)
        logger.error(Exception)
        raise HTTPException(status_code=404, detail='user not found')

@user.get('/get_my_posts/')
async def get_my_post(user = Depends(user_authorizer)):
    try:
        return await get_my_posts(user)
    except Exception:
        logger.info(user.__dict__)
        logger.exception(Exception.with_traceback)
        raise HTTPException(status_code=404, detail='the user has not any post')

@user.get('/get_queue')
async def get_queue(user = Depends(user_authorizer)):
    try:
        return await get_user_queue(user)
    except:
        logger.info(user.__dict__)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='the user queue counld not be created')
    
#TODO set signal to delete auth_user when core_userprofile is deleted
@user.delete('/delete_user/{device_id}')
async def delete_user(device_id,user=Depends(user_authorizer)):
    try:
        on_user_delete(device_id)
    except:
        logger.info(device_id)
        logger.exception(Exception)
        raise HTTPException(status_code=404, detail='the user whit this device id could not be found')

    
#-----------------------------------------------------------
@file.post("/upload_file/")
async def upload_file(uploaded_file: UploadFile = File(...)):
    uploaded_file.filename = str(uuid.uuid4())
    file_location = f"images/{uploaded_file.filename}.png"
    with open(file_location, "wb+") as file_object:
         file_object.write(uploaded_file.file.read())
    return uploaded_file.filename

@file.get("/{file_id}")
async def get_file(file_id: str, user = Depends(user_authorizer)):
    return FileResponse("images/"+file_id+'.png')


#------------------------------------------------------------

@post.post("/create/", status_code=201)
async def create_new_post(request: CreatePost,user = Depends(user_authorizer)) -> Any:   
    try:
        return await create_post(request,user)
    except Exception:
        logger.error('the object with following data could not be created')
        logger.info(request)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='Object Cannot be created with this data')

@post.get("/get_post/{post_id}")
async def get_post(post_id: int, user = Depends(user_authorizer)):
    try:
        post = await get_post_by_id(post_id)
    except Exception:
        logger.info(post_id)
        logger.exception(Exception)
        raise HTTPException(status_code=404, detail="Post not found")
    return post

#TODO: CHANGE THIS FUCKING BAD DEFINED SET_IMAGE
@post.put("/set_image/", status_code=201)
async def set_image(request: ImagePost, user: user = Depends(user_authorizer)):
	post = await _post.get(id = request.post_id)
	if request.gnerated:
		post.generated_image = await request.file_id
	else:
		post.uploaded_image = await request.file_id
	return await post.__dict__

@post.get("/get_image/{post_id}/{generated}")
async def get_image_by_post_id(post_id:int, generated: bool = 0) -> Any:
    post =  await get_post_by_id(post_id)
    if generated:
        path = "images/"+str(post.generated_image)+'.png'
    else:
        path = "images/"+str(post.uploaded_image)+'.png'
    try:
        return FileResponse(path)
    except Exception:
        logger.info(post_id)
        logger.exception(Exception)
        raise HTTPException(status_code=404, detail="image not found")

@post.put('/intract/')
async def post_interact(request: IntractPost, user = Depends(user_authorizer)):
    try:
        post = await get_post_by_id(request.post_id)
    except ObjectDoesNotExist:
        logger.info(request,user)
        logger.exception(ObjectDoesNotExist)
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        if await has_user_interacted(user, post):
            logger.info(request)
            logger.info(user.__dict__)
            return {"status": 0, "message":'already interacted with this post'}
    except Exception:
        logger.info(request)
        logger.info(user.__dict__)
        logger.error(Exception)
        raise HTTPException(status_code=500, detail="There is an error with loading interactions")
    try:
        await on_post_intract_update(user,post,request.isLike)
    except IntegrityError:
        logger.info(request,user)
        logger.exception(IntegrityError)
        logger.error('Failed to save the changes due to a conflict')
        raise HTTPException(status_code=409, detail="Conflict")
    except Exception:
        logger.info(request,user)
        logger.error(Exception)
        raise HTTPException(status_code=500, detail='There is an error with saving interactions')
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

@topic.post("/create/", status_code=201)
async def create_new_topic(request: TopicInCreate, user  = Depends(user_authorizer)) -> Any:
    try:
        return await create_topic(title = request.title)
    except Exception:
        logger.error('the object with following data could not be created')
        logger.info(request)
        logger.exception(Exception)
        raise HTTPException(status_code=400, detail='Object Cannot be created with this data')

@topic.delete("/delete_topic/{topic_id}",status_code=200)
async def delete_topic(topic_id, user = Depends(user_authorizer)):
    on_delete_topic(topic_id)