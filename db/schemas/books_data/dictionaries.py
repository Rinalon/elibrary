from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field

from db.schemas.response_base_model import ResponseModel

# ===== Language =====
class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    language_id: int
    title: str

class LanguageCreate(BaseModel):
    title: str = Field(min_length=2, max_length=32)

# ===== Publisher =====
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

class PublisherCreate(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    link: str = Field(min_length=2, max_length=256)