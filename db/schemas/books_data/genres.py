from __future__ import annotations
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel

class GenreShortResponse(ResponseModel):
    genre_id: int
    title: str

class GenreResponse(ResponseModel):
    """Схема для получения данных о жанре"""
    genre_id: int
    title: str
    description: Optional[str] = None
    books: Optional[List["BookShortResponse"]] = None

