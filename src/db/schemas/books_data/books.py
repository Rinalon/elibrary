from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from src.db.models.base import AgeRating
from src.db.schemas.response_base_model import ResponseModel

from src.db.schemas.books_data.authors import AuthorShortResponse
from src.db.schemas.books_data.genres import GenreShortResponse
from src.db.schemas.books_data.reviews import ReviewResponse

# ====== Create =====
class BookCreate(BaseModel):
    """Схема для создания книги"""
    title: str = Field(min_length=1, max_length=256)
    description: Optional[str] = Field(None, max_length=1024)
    year_of_publish: int = Field(ge=0, le=datetime.now().year)
    publisher_id: int
    language_id: int
    age_rating: Optional[AgeRating] = None
    price: Decimal = Field(ge=0)
    text_url: Optional[str] = Field(None, max_length=256)
    cover_url: Optional[str] = Field(None, max_length=256)
    author_ids: Optional[List[int]] = Field(None)
    genre_ids: Optional[List[int]] = Field(None)

# ====== Update ======
class BookUpdate(BaseModel):
    """Схема для обновления книги"""
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = Field(None, max_length=1024)
    year_of_publish: Optional[int] = Field(None, ge=0, le=datetime.now().year)
    publisher_id: Optional[int] = None
    language_id: Optional[int] = None
    age_rating: Optional[AgeRating] = None
    price: Optional[Decimal] = Field(None, ge=0)
    text_url: Optional[str] = Field(None, max_length=256)
    cover_url: Optional[str] = Field(None, max_length=256)
    author_ids: Optional[List[int]] = Field(None, min_length=1)
    genre_ids: Optional[List[int]] = Field(None, min_length=1)

# ====== Response =====
class BookShortResponse(ResponseModel):
    """Схема для получения части информации о книге"""
    book_id: int
    title: str
    cover_url: Optional[str] = None
    rating: Optional[float] = None

class BookResponse(ResponseModel):
    """Схема для получения данных о книге"""
    title: str
    description: Optional[str] = None
    year_of_publish: int
    age_rating: Optional[AgeRating] = None
    price: Decimal
    cover_url: Optional[str] = None
    text_url: Optional[str] = None
    rating: Optional[float] = None
    watched: int
    language: str = Field(alias="language_name")
    publisher: str = Field(alias="publisher_name")
    authors: Optional[List["AuthorShortResponse"]] = None
    genres: Optional[List["GenreShortResponse"]] = None
    reviews: Optional[List["ReviewResponse"]] = None


# ====== Filter =====
class BookFilter(ResponseModel):
    """Схема для фильтрации книг"""
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    author_id: Optional[int] = None
    genre_id: Optional[int] = None
    publisher_id: Optional[int] = None
    language_id: Optional[int] = None
    age_rating: Optional[AgeRating] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    limit: int = Field(10, ge=5, le=20)
    offset: int = Field(0, ge=0)

    @model_validator(mode="after")
    def validate_price_range(self) -> Optional[Decimal]:
        if self.min_price and self.max_price:
            if self.min_price > self.max_price:
                raise ValueError("min_price must be <= max_price")

