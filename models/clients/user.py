from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Date,
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
from models.base import Base

class User(Base):
    """
        Модель пользователя в системе.

        Хранит учётные данные и связи с другими сущностями.

        Attributes:
            user_id (int): Уникальный идентификатор пользователя
            login (str): Уникальный логин (от 6 до 256 символов)
            password_hash (str): Хеш пароля
            nickname (str): Отображаемое имя пользователя
            organisation_id (Optional[int]): ID организации (если пользователь принадлежит к организации)
            created_at (datetime): Дата и время регистрации
    """
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(login) >= 6", name="users_login_check"),
        Index("users_organisation_id_idx", "organisation_id"),
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

    organisation_id : Mapped[Optional[int]] = mapped_column(
        SmallInteger,
        ForeignKey(
            "clients.organisations.organisation_id",
                   deferrable=True,
                   initially="IMMEDIATE"
        ),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    user_books: Mapped[list["Book"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    organization: Mapped["Organization"] = relationship(back_populates="user", uselist=False)
    cheques: Mapped[list["Cheque"]] = relationship(back_populates="user")
    personal_data: Mapped["Personaldata"] = relationship(back_populates="user")

class Personaldata(Base):
    """
        Модель персональных данных.
        Создана для изоляции персональных данных пользователя, что позволяет быстро удалить эти данные по запросу пользователя.

        Хранит контакты для двойной аутентификации, ФИО и платёжные средства пользователя.
        Несмотря на опциональность полей email и phonenumber, что-то одно из них должно быть. Соответствующие проверки есть на уровне API и БД.
        Attributes:
            user_id (int): Уникальный идентификатор пользователя (ссылается на такой же user_id из таблицы Users)
            email (Optional[str]): Email пользователя (опционально)
            phonenumber (Optional[str]): Телефон пользователя (опционально)
            surname (str): Фамилия пользователя
            first_name (str): Имя пользователя
            second_name (str): Отчество пользователя
            birthdate (date): Дата рождения пользователя
            payment (Optional[dict]): Платёжные данные в формате JSON
    """
    __tablename__ = "personal_data"
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
        CheckConstraint(
            "birthdate BETWEEN '1900-01-01'::date AND CURRENT_DATE",
            name="ck_personal_data_birthdate_check"
        ),
        Index("personaldata_payment_idx", "payment", postgresql_using='gin'),
        {"schema": "clients"}
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clients.users.user_id",),
        primary_key=True,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(256),
        unique = True,
    )

    phonenumber: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
    )

    surname: Mapped[Optional[str]] = mapped_column(
        String(256),
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(256),
    )
    second_name: Mapped[Optional[str]] = mapped_column(
        String(256),
    )

    birthdate: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    payment: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="personal_data")


