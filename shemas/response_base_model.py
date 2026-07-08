from pydantic import BaseModel, ConfigDict

class ResponseModel(BaseModel):
    """Базовый класс для всех Pydantic-схем, работающих с SQLAlchemy."""
    config = ConfigDict(from_attributes=True)