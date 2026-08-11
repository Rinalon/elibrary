from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

from src.db.schemas.response_base_model import ResponseModel

class PublisherShortResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    publisher_id: int
    name: str

class PublisherResponse(ResponseModel):
    """Схема для получения данных об издателе"""
    name: str
    link: str
    books: List["BookShortResponse"]

class PublisherCreate(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    link: str = Field(min_length=2, max_length=256)

class PublisherUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=64)
    link: Optional[str] = Field(min_length=2, max_length=256)