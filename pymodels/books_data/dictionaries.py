from sqlalchemy import SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column
from pymodels.base import Base

class Languages(Base):
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

class Publishers(Base):
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
