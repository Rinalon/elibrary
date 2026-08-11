from pydantic import BaseModel, Field
from datetime import timedelta
from typing import Optional
from decimal import Decimal
from src.db.schemas.response_base_model import ResponseModel

# ====== Create =====
class SubscribeTypeCreate(BaseModel):
    """Схема для создания подписки"""
    title: str = Field(min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Decimal = Field(ge=0)
    duration_days: int = Field(ge=1)
    book_ids: list[int]

# ====== Update =====
class SubscribeUpdate(BaseModel):
    """Схема для изменения подписки"""
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Optional[Decimal] = Field(None, ge=0)
    duration_days: Optional[int] = Field(None, ge=1)
    book_ids: Optional[list[int]] = None

# ====== Response =====
class SubscribeTypeResponse(ResponseModel):
    """Схема для получения данных подписки"""
    id: int
    title: str
    info: Optional[str]
    price: Decimal
    duration: timedelta
