from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from db.schemas.response_base_model import ResponseModel

class ReviewCreate(BaseModel):
    """Схема для создания отзыва"""
    book_id: int
    review: Optional[str] = Field(None, max_length=4096)
    rating: int = Field(ge=0, le=5)

class ReviewEdit(BaseModel):
    """Схема для редактирования отзыва"""
    review: Optional[str] = Field(None, max_length=4096)
    rating: int = Field(ge=0, le=5)

class ReviewResponse(ResponseModel):
    """Схема для получения отзыва"""
    review_id: int
    user_name: str
    rating: int
    review: Optional[str]