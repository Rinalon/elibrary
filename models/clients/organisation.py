from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    CheckConstraint,
    func,
    SmallInteger
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from models.base import Base

class Organisation(Base):
    """
        Модель организаций.

        Хранит информацию об организации и связи с другими сущностями.

        Attributes:
            owner_id (int): Идентификатор владельца организации (ссылается на user_id в Users)
            organisation_id (int): Уникальный идентификатор организации
            organisation_name (str): Название организации
            created_at (datetime): Дата создания органиации в системе

    """
    __tablename__ = 'organisations'
    __table_args__ = (
        Index("organisations_owner_id_idx", "owner_id"),
        {"schema": "clients"}
    )

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.users.user_id",
            deferrable=True,
            initially="IMMEDIATE"
        ),
        unique = True,
        nullable = False,
    )

    organisation_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        server_default=func.identity()
    )

    organisation_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    contracts: Mapped[list["Contract"]] = relationship(back_populates="organisation")

    users: Mapped[list["User"]] = relationship(
        back_populates="organisation",
        foreign_keys="User.organisation_id"
    )

    owner: Mapped["User"] = relationship(
        back_populates="owned_organisation",
        uselist=False,
        foreign_keys=[owner_id]
    )
