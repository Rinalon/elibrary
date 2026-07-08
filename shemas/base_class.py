from pydantic import BaseModel, ConfigDict

class ORMModel(BaseModel):
    """Базовый класс для всех Pydantic-схем, работающих с SQLAlchemy."""
    config = ConfigDict(from_attributes=True)