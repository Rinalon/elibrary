from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta
from typing import List, Optional, Literal
from decimal import Decimal
from response_base_model import ResponseModel

class ChequeItemBase(BaseModel):
    type: Literal["book", "contract"]
    cost: Decimal
    id: int
    item_name: str

class ChequeBookItem(ChequeItemBase):
    type: Literal["book"] = "book"

class ChequeContractItem(ChequeItemBase):
    type: Literal["contract"] = "contract"

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

class ChequeCreate(BaseModel):
    """"""
    user_id: int = Field(alias='payer')
    total_cost: Decimal = Field(ge=0)
    cheque_info: int
    items: List[ChequeBookItem | ChequeContractItem] = Field(default_factory=list)

# ====== Response =====
class SubscribeTypeResponse(ResponseModel):
    id: int
    title: str
    info: Optional[str]
    price: Decimal
    duration: timedelta

class ContractResponse(ResponseModel):
    contract_id: int
    subscribe_name: str
    organisation_name: str
    total_cost: Decimal
    contract_info: Optional[str]
    start_date: date
    end_date: date
    contract_date: date

class ChequeResponse(ResponseModel):
    cheque_id: int
    cheque_date: datetime
    items: List[ChequeBookItem | ChequeContractItem] = Field(default_factory=list)
    total_cost: Decimal
    cheque_info: str