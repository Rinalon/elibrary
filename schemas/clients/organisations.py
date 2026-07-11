from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from schemas.response_base_model import ResponseModel

class OrganisationCreate(BaseModel):
    owner_id: int = Field(alias="creator", ge=1)
    organisation_name: str = Field(
        alias="name",
        min_length=5,
        max_length=64
    )
    members: Optional[list[int]]

class OrganisationEdit(BaseModel):
    organisation_name: Optional[str] = Field(
        alias="name",
        min_length=5,
        max_length=64
    )
    members: Optional[List["UserShortResponse"]]

class OrganisationResponse(ResponseModel):
    organisation_id: int
    owner_id: int = Field(alias="creator")
    organisation_name: str
    members: Optional[List["UserShortResponse"]]
    contracts: Optional[List["ContractShortResponse"]]
    created: datetime

