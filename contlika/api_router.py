from celestial.endpoints import user as user_router
from celestial.endpoints import post as post_router 
from celestial.endpoints import file as file_router
from celestial.endpoints import topic as topic_router


from fastapi import APIRouter

celestial_router = APIRouter()

celestial_router.include_router(user_router, prefix="/user", tags=["user"])
celestial_router.include_router(post_router, prefix="/post", tags=["post"])
celestial_router.include_router(file_router, prefix="/file", tags=["file"])
celestial_router.include_router(topic_router, prefix="/topic", tags=["topic"])