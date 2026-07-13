from __future__ import annotations
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel


class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    language_id: int
    title: str

class PublisherShortResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    publisher_id: int
    name: str

class PublisherResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    publisher_id: int
    name: str
    link: str
    books: List["BookShortResponse"]