from ast import Dict
from typing import List, Optional
from pydantic import BaseModel

class PostFromCelestial(BaseModel):
    prompt: str
    n_prompt: Optional[str]
    image: str

class PostForSelestial(BaseModel):
    images: Dict

class DiffusersIn(BaseModel):
    seed: Optional[int]
    model_address: Optional[str]
    strength: Optional[str]
    prompt: str
    helper_prompt: Optional[str]
    n_prompt: Optional[str]
    image: str

class DiffusersOut(BaseModel):
    images: List