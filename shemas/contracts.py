from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta
from typing import List, Optional, Literal
from decimal import Decimal
from response_base_model import ResponseModel

# ====== Create =====
class SubscribeTypeCreate(BaseModel):
    """Схема для создания подписки"""
    title: str = Field(min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Decimal = Field(ge=0)
    duration_days: int = Field(ge=1)
    book_ids: list[int]

class ContractCreate(BaseModel):
    """Схема для создания контракта"""
    subscribe_id: int
    organisation_id: int
    contract_info: Optional[str] = Field(None, max_length=256)
    start_date: date
    end_date: date
    total_cost: Decimal = Field(ge=0)

# ====== Update =====
class SubscribeUpdate(BaseModel):
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

class ContractResponse(ResponseModel):
    """Схема для получения данных контракта"""
    contract_id: int
    subscribe_name: str
    organisation_name: str
    total_cost: Decimal
    contract_info: Optional[str]
    start_date: date
    end_date: date
    contract_date: date

class ContractShortResponse(ResponseModel):
    """Схема для получения части данных контракта"""
    contract_id: int
    subscribe_name: str
    start_date: date
    end_date: date
    contract_date: date