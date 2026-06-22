from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    SmallInteger,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Index,
    CheckConstraint,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy import Enum
from pymodels.base import Base, AgeRating

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint(
            "year_of_publish BETWEEN 0 AND EXTRACT(YEAR FROM CURRENT_DATE)",
                    name="books_year_of_publish_check"),
        CheckConstraint(
            "price >= 0::money",
            name="books_price_check"
        ),
        Index("books_title_idx",
              "title",
              postgresql_using="gin",
              postgresql_ops={"title": "gin_trgm_ops"}
        ),
        Index("books_price_idx", "price"),
        Index("books_language_id_idx", "language_id"),
        Index("books_publisher_id_idx", "publisher_id"),
        {"schema": "books_data"},
    )

    book_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()  # GENERATED ALWAYS AS IDENTITY
    )

    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True
    )

    year_of_publish: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    publisher_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "books_data.publishers.publisher_id",
            deferrable=True,
            initially="IMMEDIATE"  # DEFERRABLE INITIALLY IMMEDIATE
        ),
        nullable=False
    )

    language_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "books_data.languages.language_id",
            deferrable=True,
            initially="IMMEDIATE"
        ),
        nullable=False
    )

    age_rating: Mapped[Optional[AgeRating]] = mapped_column(
        Enum(AgeRating, name="age_rating_enum", schema="public"),
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        MONEY,
        nullable=False,
        server_default="0.00",
    )

    text_url: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True
    )

    cover_url: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    publisher: Mapped["Publisher"] = relationship(back_populates="books")
    language: Mapped["Language"] = relationship(back_populates="books")
    changeable: Mapped["BookChangeable"] = relationship(back_populates="book", uselist=False)
    authors: Mapped[list["Author"]] = relationship(
        secondary="books_data.author_book",
        back_populates="books"
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary="books_data.book_genre",
        back_populates="books"
    )
    cheques: Mapped[list["Cheque"]] = relationship(
        secondary="payments_data.cheque_book",
        back_populates="books"
    )
    subscriptions: Mapped[list["SubscribeType"]] = relationship(
        secondary="subscribes_data.subscribe_book",
        back_populates="subscriptions"
    )
    reviews: Mapped[list["Review"]] = relationship(back_populates="book")
    user_books: Mapped[list["UserBook"]] = relationship(back_populates="book")

class BookChangeable(Base):
    __tablename__ = "books_changeable"
    __table_args__ = (
        Index("idx_books_changeable_rating", "rating"),
        Index("idx_books_changeable_watched", "watched"),
        {"schema": "books_data"}
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

    rating: Mapped[float] = mapped_column(
        Numeric(3,2),
        nullable=True,
        check="rating >= 0.00 AND rating <= 5.00",
        server_default="0.00"
    )

    watched: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        check="watched >= 0",
        server_default="0",
    )

    book: Mapped["Book"] = relationship(back_populates="changeable", uselist=False)