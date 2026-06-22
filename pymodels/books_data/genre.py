from typing import Optional
from sqlalchemy import SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column
from pymodels.base import Base

class Genres(Base):
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
