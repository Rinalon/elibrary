from pydantic import BaseModel, Field
from datetime import date, timedelta
from typing import Optional
from decimal import Decimal


class SubscribeTypeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    info: Optional[str] = Field(None, max_length=512)
    price: Decimal = Field(ge=0)
    duration_days: int = Field(ge=1, description="Длительность подписки в днях")
    book_ids: list[int] = Field(description="Книги, доступные по подписке")


class SubscribeTypeResponse(BaseModel):
    id: int
    title: str
    info: Optional[str]
    price: Decimal
    duration: timedelta
    created_at: date

    model_config = {"from_attributes": True}


class ContractCreate(BaseModel):
    subscribe_id: int
    organisation_id: int


class ContractResponse(BaseModel):
    contract_id: int
    subscribe_id: int
    organisation_id: int
    total_cost: Decimal
    start_date: date
    end_date: date
    contract_date: date

    model_config = {"from_attributes": True}