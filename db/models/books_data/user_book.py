from sqlalchemy import Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import Base

class UserBook(Base):
    """
        Модель таблицы связи книги и пользователя в системе.

        Attributes:
            user_id (int): Идентификатор пользователя (ссылается на user_id в Users)
            book_id (int): Идентификатор книги (ссылается на book_id в Books)
            percentage (float): Прогресс чтения книги
    """
    __tablename__ = "user_book"
    __table_args__ = (
        CheckConstraint(
            "percentage >= 0.00 AND percentage <= 100.00",
            "user_book_percentage_check"
        ),
        {"schema": "books_data"}
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.users.user_id",
            deferrable=True,
            initially="IMMEDIATE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "books_data.books.book_id",
            deferrable=True,
            initially="IMMEDIATE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    percentage: Mapped[float] = mapped_column(
        Numeric(5,2),
        nullable=False,
        server_default="0.00"
    )

    book: Mapped["Book"] = relationship(back_populates="user_books", uselist=False)
    user: Mapped["User"] = relationship(back_populates="user_books", uselist=False)
