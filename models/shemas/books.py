from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from models.base import AgeRating


# === SCHEMAS FOR CREATION ===
class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    description: Optional[str] = Field(None, max_length=1024)
    year_of_publish: int = Field(ge=0, le=datetime.now().year)
    publisher_id: int
    language_id: int
    age_rating: Optional[AgeRating] = None
    price: Decimal = Field(ge=0, description="Цена в рублях")
    text_url: Optional[str] = Field(None, max_length=256)
    cover_url: Optional[str] = Field(None, max_length=256)
    author_ids: List[int] = Field(min_length=1, description="ID авторов")
    genre_ids: List[int] = Field(min_length=1, description="ID жанров")


# === SCHEMAS FOR RESPONSE ===
class BookResponse(BaseModel):
    book_id: int
    title: str
    description: Optional[str]
    year_of_publish: int
    age_rating: Optional[AgeRating]
    price: Decimal
    rating: Optional[Decimal]
    watched: int

    # Вложенные объекты (опционально, если нужны полные данные)
    authors: Optional[List["AuthorResponse"]] = None
    genres: Optional[List["GenreResponse"]] = None

    model_config = {"from_attributes": True}


# === SCHEMAS FOR FILTER ===
class BookFilter(BaseModel):
    """Схема для фильтрации книг"""
    title: Optional[str] = Field(None, description="Поиск по названию (частичное совпадение)")
    author_id: Optional[int] = None
    genre_id: Optional[int] = None
    publisher_id: Optional[int] = None
    language_id: Optional[int] = None
    age_rating: Optional[AgeRating] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    min_year: Optional[int] = Field(None, ge=0)
    max_year: Optional[int] = Field(None, le=datetime.now().year)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)

    @field_validator("min_price", "max_price")
    @classmethod
    def validate_price_range(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        if info.data.get("min_price") and info.data.get("max_price"):
            if info.data["min_price"] > info.data["max_price"]:
                raise ValueError("min_price must be <= max_price")
        return v