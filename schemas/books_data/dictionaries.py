from typing import Optional, List
from schemas.response_base_model import ResponseModel


class GenreResponse(ResponseModel):
    """Схема для получения данных о жанре"""
    name: str
    description: Optional[str] = None
    most_popular_books: Optional[List["BookResponse"]] = None

class AuthorResponse(ResponseModel):
    """Схема для получения данных об авторе"""
    name: str
    description: Optional[str] = None
    books: Optional[List["BookResponse"]] = None

class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    language_id: int
    title: str

class PublisherResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    publisher_id: int
    name: str
    link: str