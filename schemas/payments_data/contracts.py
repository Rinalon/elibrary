from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal
from schemas.response_base_model import ResponseModel

# ====== Create =====
class ContractCreate(BaseModel):
    """Схема для создания контракта"""
    subscribe_id: int
    organisation_id: int
    contract_info: Optional[str] = Field(None, max_length=256)
    start_date: date
    end_date: date
    total_cost: Decimal = Field(ge=0)

# ====== Response =====
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