from core.endpoints import user as user_router
from core.endpoints import post as post_router 
from core.endpoints import file as file_router
from core.endpoints import topic as topic_router


from fastapi import APIRouter

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(post_router, prefix="/post", tags=["post"])
router.include_router(file_router, prefix="/file", tags=["file"])
router.include_router(topic_router, prefix="/topic", tags=["topic"])