from sqlalchemy import SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

class Publisher(Base):
    """
        Модель издателей книг в системе.

        Attributes:
            publisher_id (int): Уникальный идентификатор издателя
            name (str): Название издательства
            link (str): Ссылка на сайт издательства
    """
    __tablename__ = "publishers"
    __table_args__ = (
        {"schema": "books_data"}
    )

    publisher_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        server_default=func.identity()
    )

    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    link: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    books: Mapped[list["Book"]] = relationship(back_populates="publisher")