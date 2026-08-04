from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from src.db.schemas.response_base_model import ResponseModel

class GenreShortResponse(ResponseModel):
    genre_id: int
    title: str

class GenreResponse(ResponseModel):
    """Схема для получения данных о жанре"""
    title: str
    description: Optional[str] = None
    books: Optional[List["BookShortResponse"]] = None

class GenreCreate(BaseModel):
    title: str = Field(min_length=2, max_length=32)
    description: Optional[str] = Field(None, min_length=2, max_length=512)
    books: Optional[List[int]] = None

