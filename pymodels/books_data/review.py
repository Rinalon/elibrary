from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    SmallInteger,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from pymodels.base import Base

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="reviews_user_id_book_id_key"),
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

    rating: Mapped[float] = mapped_column(
        Numeric(3,2),
        nullable=False,
        check="rating >= 0.00 AND rating <= 5.00",
        server_default="0.00"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    book: Mapped["Book"] = relationship(back_populates="reviews", uselist=False)