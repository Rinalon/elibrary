from __future__ import annotations
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel

class AuthorShortResponse(ResponseModel):
    author_name: str

class AuthorResponse(ResponseModel):
    """Схема для получения данных об авторе"""
    author_name: str
    description: Optional[str] = None
    books: Optional[List["BookShortResponse"]] = None