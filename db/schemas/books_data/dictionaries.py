from __future__ import annotations
from typing import Optional, List
from db.schemas.response_base_model import ResponseModel


class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    title: str

class PublisherShortResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    name: str

class PublisherResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    name: str
    link: str
    books: List["BookShortResponse"]