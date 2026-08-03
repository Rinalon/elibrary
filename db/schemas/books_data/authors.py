from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel

class AuthorShortResponse(ResponseModel):
    author_id: int
    author_name: str

class AuthorResponse(ResponseModel):
    """Схема для получения данных об авторе"""
    author_name: str
    author_info: Optional[str] = None
    books: Optional[List["BookShortResponse"]] = None

class AuthorCreate(BaseModel):
    author_name: str = Field(min_length=2,max_length=256)
    author_info: Optional[str] = Field(
        None,
        min_length=2,
        max_length=1024
    )
    books: Optional[List[int]] = None

