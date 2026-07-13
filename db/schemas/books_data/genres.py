from __future__ import annotations
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel

class GenreShortResponse(ResponseModel):
    title: str

class GenreResponse(ResponseModel):
    """Схема для получения данных о жанре"""
    title: str
    description: Optional[str] = None
    most_popular_books: Optional[List["BookShortResponse"]] = None

