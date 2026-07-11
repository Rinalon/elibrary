from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from models.base import AgeRating
from schemas.response_base_model import ResponseModel

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
    author_ids: List[int] = Field(min_length=1)
    genre_ids: List[int] = Field(min_length=1)

# ====== Update | Edit =====
class BookEdit(BaseModel):
    """Схема для обновления книги"""
    title: Optional[str] = Field(min_length=1, max_length=256)
    description: Optional[str] = Field(None, max_length=1024)
    year_of_publish: Optional[int] = Field(ge=0, le=datetime.now().year)
    publisher_id: Optional[int]
    language_id: Optional[int]
    age_rating: Optional[AgeRating] = None
    price: Optional[Decimal] = Field(ge=0)
    text_url: Optional[str] = Field(None, max_length=256)
    cover_url: Optional[str] = Field(None, max_length=256)
    author_ids: Optional[List[int]] = Field(min_length=1)
    genre_ids: Optional[List[int]] = Field(min_length=1)

class UserBookUpdate(BaseModel):
    """Схема для обновлений прогресса чтения"""
    percentage: float = Field(ge=0, le=100)

# ====== Response =====
class BookResponse(ResponseModel):
    """Схема для получения данных о книге"""
    book_id: int
    title: str
    description: Optional[str]
    year_of_publish: int
    age_rating: Optional[AgeRating]
    price: Decimal
    cover_url: Optional[str]
    text_url: Optional[str]
    rating: Optional[float]
    watched: int
    authors: Optional[List["AuthorResponse"]] = None
    genres: Optional[List["GenreResponse"]] = None
    reviews: Optional[List["ReviewResponse"]] = None


# ====== Filter =====
class BookFilter(ResponseModel):
    """Схема для фильтрации книг"""
    title: Optional[str] = None
    author_id: Optional[int] = None
    genre_id: Optional[int] = None
    publisher_id: Optional[int] = None
    language_id: Optional[int] = None
    age_rating: Optional[AgeRating] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    limit: int = Field(10, ge=5, le=20)
    offset: int = Field(0, ge=0)

    @field_validator("min_price", "max_price")
    @classmethod
    def validate_price_range(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        if info.data.get("min_price") and info.data.get("max_price"):
            if info.data["min_price"] > info.data["max_price"]:
                raise ValueError("min_price must be <= max_price")
        return v