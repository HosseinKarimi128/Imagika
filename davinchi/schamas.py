from ast import Dict
from typing import Optional
from pydantic import BaseModel

class PostFromCelestial(BaseModel):
    prompt: str
    n_prompt: Optional[str]
    image: str

class PostForSelestial(BaseModel):
    images: Dict