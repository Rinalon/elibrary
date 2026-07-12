from typing import Optional
from sqlalchemy import (
    SmallInteger,
    String,
    func,
    Table,
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import Base

class Genre(Base):
    """
        Модель жанров в системе.

        Attributes:
            genre_id (int): Уникальный идентификатор жанра
            title (str): Название жанра
            description (str): Описание жанра
    """
    __tablename__ = "genres"
    __table_args__ = (
        {"schema": "books_data"}
    )

    genre_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        server_default=func.identity()
    )

    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
    )

    books: Mapped[list["Book"]] = relationship(
        secondary="books_data.book_genre",
        back_populates="genres"
    )

# Ассоциативная таблица для связи книг и жанров (М-М).
#
# Эта таблица связывает:
# - genres (жанры) — genre_id
# - books (книги) — book_id
#
# Используется для того, чтобы у книги могло быть несколько жанров,
# и у жанров могло быть несколько книг.
book_genre = Table(
    "book_genre",
    Base.metadata,
    Column(
        "book_id",
           Integer,
           ForeignKey(
               "books_data.books.book_id",
                ondelete="CASCADE",
                deferrable=True,
                initially="IMMEDIATE"
                ),
           primary_key=True
    ),
    Column(
        "genre_id",
        SmallInteger,
        ForeignKey(
            "books_data.genres.genre_id",
            ondelete="CASCADE",
            deferrable=True,
            initially="IMMEDIATE"
            ),
        primary_key=True
    ),
    schema="books_data"
)
