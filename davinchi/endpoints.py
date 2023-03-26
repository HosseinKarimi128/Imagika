import logging
from fastapi import APIRouter, Depends
from davinchi.schemas import *
from davinchi.services import *
from celestial.endpoints import user_authorizer
from fastapi.security import HTTPBearer

generate = APIRouter()
logger = logging.getLogger(__name__)
security = HTTPBearer()

@generate.post('/generate_image/', status_code = 201)
async def generate_image(request:PostFromCelestial) -> PostForCelestial:
    res = await on_generate_image(request)
    await logger.info(res)
    return await PostForCelestial(images = res)
    # return Image.open(BytesIO(request.image.encode())).convert("RGB")