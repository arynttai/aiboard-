from typing import Optional, List
from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    author: str
    text: str
    keywords: str


class EditPostRequest(BaseModel):
    author: Optional[str] = None
    text: Optional[str] = None
    keywords: Optional[str] = None


    
    
