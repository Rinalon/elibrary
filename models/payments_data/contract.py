from datetime import date
from typing import Optional
from sqlalchemy import (
    Index,
    Integer,
    SmallInteger,
    String,
    Date,
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

class Contract(Base):
    """
        Модель контракта подписки в системе.

        Хранит данные контракта и связи с другими сущностями.

        Attributes:
            contract_id: Уникальный идентификатор контракта
            subscribe_id (int): Идентификатор подписки (ссылается на subscribe_id в Subscribe_types)
            organisation_id (int): Идентификатор пользователя (ссылается на organisation_id в Organisations)
            total_cost (float): Полная стоимость контракта
            start_date (datetime): Дата начала действия подписки
            end_date (datetime): Дата конца действия подписки и контракта
            contract_info (Optional[str]): информация о контракте и/или прочая информация
            contract_date (datetime): Дата заключения контракта
    """
    __tablename__ = "contracts"
    __table_args__ = (
        Index("contracts_contract_date_idx", "contract_date"),
        Index("contracts_end_date_idx", "end_date"),
        Index("contracts_organisation_id_idx", "organisation_id"),
        Index("contracts_subscribe_id_idx", "subscribe_id"),
        CheckConstraint(
            "start_date >= contract_date AND contract_date <= CURRENT_DATE",
            name="contract_date_logic"
        ),
        CheckConstraint("total_cost >= 0::money", "contracts_total_cost_check"),
        CheckConstraint("end_date > start_date", "contracts_end_date_check"),
        {"schema": "payments_data"}
    )

    contract_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()
    )

    subscribe_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "subscribes_data.subscribe_types.id",
            deferrable=True,
            initially="IMMEDIATE",
        ),
        nullable=False,
    )

    organisation_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "clients.organisations.organisation_id",
            deferrable=True,
            initially="IMMEDIATE",
        ),
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        Numeric,
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    contract_info: Mapped[Optional[str]] = mapped_column(String(256))

    contract_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )

    subscribe: Mapped["SubscribeType"] = relationship(back_populates="contracts", uselist=False)
    organisation: Mapped["Organisation"] = relationship(back_populates="contracts", uselist=False)
    cheque: Mapped["Cheque"] = relationship(
        secondary="payments_data.cheque_contract",
        back_populates="contracts",
        uselist=False
    )