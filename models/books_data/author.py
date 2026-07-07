from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from models.base import Base

class Author(Base):
    __tablename__ = "authors"
    __table_args__ = (
        Index("authors_author_name_idx",
              "author_name",
              postgresql_using="gin",
              postgresql_ops={"author_name": "gin_trgm_ops"}
        ),
        {"schema": "books_data"}
    )

    author_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()
    )

    author_name: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )

    author_info: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    books: Mapped[list["Book"]] = relationship(
        secondary="books_data.author_book",
        back_populates="authors"
    )

author_book = Table(
    "author_book",
    Base.metadata,
    Column(
        "author_id",
           Integer,
           ForeignKey(
               "books_data.authors.author_id",
                ondelete="CASCADE",
                deferrable=True,
                initially="IMMEDIATE"
                ),
           primary_key=True
    ),
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
    schema="books_data"
)