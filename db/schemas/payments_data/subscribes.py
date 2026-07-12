from pydantic import BaseModel, Field
from datetime import timedelta
from typing import Optional
from decimal import Decimal
from db.schemas.response_base_model import ResponseModel

# ====== Create =====
class SubscribeTypeCreate(BaseModel):
    """Схема для создания подписки"""
    title: str = Field(min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Decimal = Field(ge=0)
    duration_days: int = Field(ge=1)
    book_ids: list[int]

# ====== Edit =====
class SubscribeEdit(BaseModel):
    """Схема для изменения подписки"""
    title: Optional[str] = Field(min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Optional[Decimal] = Field(ge=0)
    duration_days: Optional[int] = Field(ge=1)
    book_ids: Optional[list[int]]

# ====== Response =====
class SubscribeTypeResponse(ResponseModel):
    """Схема для получения данных подписки"""
    id: int
    title: str
    info: Optional[str]
    price: Decimal
    duration: timedelta
