from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import (
    Table,
    Column,
    Integer,
    SmallInteger,
    String,
    Interval,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import MONEY
from models.base import Base

class SubscribeType(Base):
    """
        Модель типа подписки в системе.

        Хранит данные подписки и связи с другими сущностями.

        Attributes:
            id: Уникальный идентификатор подписки
            title (int): Название подписки
            price (float): Стоимость
            info (str): Информация о подписке
            duration (timedelta): Длительност подписки
            created_at (datetime): Дата и время создания подписки
    """
    __tablename__ = "subscribe_types"
    __table_args__ = (
        CheckConstraint("price >= 0", "subscribe_types_price_check"),
        {"schema": "subscribes_data"}
    )

    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        server_default=func.identity(),
    )

    title: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    info: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        MONEY,
        nullable=False,
        server_default="0"
    )

    duration: Mapped[timedelta] = mapped_column(
        Interval,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    books: Mapped[list["Book"]] = relationship(
        secondary="subscribes_data.subscribe_book",
        back_populates="subscriptions"
    )
    contracts: Mapped[list["Contract"]] = relationship(back_populates="subscribe")

# Ассоциативная таблица для связи чеков об оплате и контрактов (М-М).
#
# Эта таблица связывает:
# - cheques (чеки) — cheque_id
# - contracts (контракты) — contract_id
subscribe_book = Table(
    "subscribe_book",
    Base.metadata,
    Column(
        "subscribe_id",
           SmallInteger,
           ForeignKey(
               "subscribes_data.subscribe_types.id",
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
    schema="subscribes_data"
)
