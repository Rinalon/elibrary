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
from sqlalchemy.dialects.postgresql import JSONB
from pymodels.base import Base

class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(login) >= 6", name="ck_users_login_length"),
        {"schema": "clients"}
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=func.identity()
    )

    login: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    nickname: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    organisation_id : Mapped[Optional[str]] = mapped_column(
        SmallInteger,
        ForeignKey("clients.organisations.organisation_id", deferrable=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

class Personaldata(Base):
    __tablename__ = "personaldata"
    __table_args__ = (
        CheckConstraint(
            "email ~ '^([\\w]+[.-]{0,1}[\\w]+)+@([a-zA-Z0-9]+([.-])*[a-zA-Z0-9]+)+\\.+[a-zA-Z]{2,}$'",
            name="ck_personal_data_email"
        ),
        CheckConstraint(
            "phonenumber ~ '^\\+\\d{11,15}$'",
            name="ck_personal_data_phone"
        ),
        CheckConstraint(
            "email IS NOT NULL OR phonenumber IS NOT NULL",
            name="email_or_phone_required",
        ),
        {"schema": "clients"}
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.users.user_id",
            deferrable = True,
            initially = "DEFERRED"
    ),
        primary_key=True,
    )

    email: Mapped[str] = mapped_column(
        String(256),
        unique = True,
    )

    phonenumber: Mapped[str] = mapped_column(
        String(20),
        unique=True,
    )

    surname: Mapped[str] = mapped_column(
        String(256),
    )
    first_name: Mapped[str] = mapped_column(
        String(256),
    )
    second_name: Mapped[str] = mapped_column(
        String(256),
    )
    payment: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )


