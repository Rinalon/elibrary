from sqlalchemy import SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

class Language(Base):
    """
        Модель языков книг в системе.

        Attributes:
            language_id (int): Уникальный идентификатор языка
            title (str): Название языка
    """
    __tablename__ = "languages"
    __table_args__ = (
        {"schema": "books_data"}
    )

    language_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        server_default=func.identity()
    )

    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )

    books: Mapped[list["Book"]] = relationship(back_populates="language")