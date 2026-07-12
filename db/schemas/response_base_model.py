from pydantic import BaseModel, ConfigDict

class ResponseModel(BaseModel):
    """Базовый класс для всех Pydantic-схем, работающих с SQLAlchemy."""
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )