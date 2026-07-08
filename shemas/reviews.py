from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from models.base import AgeRating
from response_base_model import ResponseModel

class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    review: Optional[str] = Field(None, max_length=4096)
    rating: int = Field(ge=0, le=5)


class ReviewResponse(ResponseModel):
    pass