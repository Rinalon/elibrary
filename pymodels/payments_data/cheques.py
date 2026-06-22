from datetime import datetime
from sqlalchemy import (
    Index,
    Integer,
    SmallInteger,
    String,
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
from pymodels.base import Base

class Cheque(Base):
    __tablename__ = "cheques"
    __table_args__ = (
        Index("cheques_user_id_idx", "user_id"),
        Index("cheques_cheque_date_idx", "cheque_date"),
        CheckConstraint("total_cost >= 0::money", "cheques_total_cost_check"),
        {"schema": "payments_data"}
    )

    cheque_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()
    )

    user_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "clients.users.user_id",
            deferrable=True,
            initially="IMMEDIATE",
        ),
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        MONEY,
        nullable=False
    )

    cheque_info: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    cheque_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="cheques", uselist=False)
    contracts: Mapped[list["Contract"]] = relationship(
        secondary="payments_data.cheque_contract",
        back_populates="cheque",
    )
    books: Mapped[list["Book"]] = relationship(
        secondary="payments_data.cheque_book",
        back_populates="cheques",
    )