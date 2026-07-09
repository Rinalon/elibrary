from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta
from typing import List, Optional, Literal
from decimal import Decimal
from response_base_model import ResponseModel


class ChequeItemBase(BaseModel):
    """Базовый класс для объектов в чеке"""
    type: Literal["book", "contract"]
    cost: Decimal
    id: int
    item_name: str

class ChequeBookItem(ChequeItemBase):
    """Класс для книги в чеке"""
    type: Literal["book"] = "book"

class ChequeContractItem(ChequeItemBase):
    """Класс для контракта в чеке"""
    type: Literal["contract"] = "contract"


class ChequeCreate(BaseModel):
    """Схема для создания чеков"""
    user_id: int = Field(alias='payer')
    total_cost: Decimal = Field(ge=0, alias='amount')
    cheque_info: str
    items: List[ChequeBookItem | ChequeContractItem] = Field(default_factory=list)


class ChequeResponse(ResponseModel):
    """Схема для получения чека"""
    cheque_id: int
    cheque_date: datetime
    items: List[ChequeBookItem | ChequeContractItem] = Field(default_factory=list)
    total_cost: Decimal
    cheque_info: str