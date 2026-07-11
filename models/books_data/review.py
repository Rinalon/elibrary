from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index,
    func, SmallInteger
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from models.base import Base

class Review(Base):
    """
        Модель отзывов на книги в системе.

        Attributes:
            review_id (int): Уникальный идентификатор отзыва
            user_id (int): Идентификатор пользователя (ссылается на user_id в Users)
            book_id (int): Идентификатор книги (ссылается на book_id в Books)
            review (Optional[str]): Текст отзыва
            rating (int): Оценка книги
            created_at (datetime): Дата и время создания отзыва
    """
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="reviews_user_id_book_id_key"),
        CheckConstraint("rating >= 0 AND rating <= 5", "reviews_rating_check"),
        Index("reviews_rating_idx", "rating"),
        Index("reviews_created_at_idx", "created_at"),
        {"schema": "books_data"}
    )

    review_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.users.user_id",
            deferrable=True,
            initially="IMMEDIATE"
        ),
        nullable=False
    )

    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "books_data.books.book_id",
            deferrable=True,
            initially="IMMEDIATE"
        ),
        nullable=False
    )

    review: Mapped[Optional[str]] = mapped_column(
        String(4096),
        nullable=True
    )

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    book: Mapped["Book"] = relationship(back_populates="reviews", uselist=False)
    user: Mapped["User"] = relationship(back_populates="reviews", uselist=False)

    @property
    def user_name(self) -> Optional[str]:
        return self.user.nickname if self.user else None

    @property
    def book_name(self) -> Optional[str]:
        return self.book.title if self.book else None