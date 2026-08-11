from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

from src.db.schemas.response_base_model import ResponseModel


# ===== Language =====
class LanguageResponse(ResponseModel):
    """Схема для получения языка"""
    language_id: int
    title: str


class LanguageCreate(BaseModel):
    title: str = Field(min_length=2, max_length=32)


class LanguageUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=32)