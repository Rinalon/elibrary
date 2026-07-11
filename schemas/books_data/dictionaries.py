from __future__ import annotations
from typing import Optional, List
from schemas.response_base_model import ResponseModel

class GenreShortResponse(ResponseModel):
    title: str

class GenreResponse(ResponseModel):
    """Схема для получения данных о жанре"""
    title: str
    description: Optional[str] = None
    most_popular_books: Optional[List["BookShortResponse"]] = None

class AuthorShortResponse(ResponseModel):
    author_name: str

class AuthorResponse(ResponseModel):
    """Схема для получения данных об авторе"""
    author_name: str
    description: Optional[str] = None
    books: Optional[List["BookShortResponse"]] = None

class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    language_id: int
    title: str

class PublisherResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    publisher_id: int
    name: str
    link: str