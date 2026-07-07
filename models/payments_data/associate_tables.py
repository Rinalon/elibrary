from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

# Ассоциативная таблица для связи чеков об оплате и книг (М-М).
#
# Эта таблица связывает:
# - cheques (чеки) — cheque_id
# - books (книги) — book_id
cheque_book = Table(
    "cheque_book",
    Base.metadata,
    Column(
        "cheque_id",
           Integer,
           ForeignKey(
               "payments_data.cheques.cheque_id",
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
            deferrable=True,
            initially="IMMEDIATE"
            ),
        primary_key=True
    ),
    schema="payments_data"
)

# Ассоциативная таблица для связи чеков об оплате и контрактов (М-М).
#
# Эта таблица связывает:
# - cheques (чеки) — cheque_id
# - contracts (контракты) — contract_id
cheque_contract = Table(
    "cheque_contract",
    Base.metadata,
    Column(
        "cheque_id",
           Integer,
           ForeignKey(
               "payments_data.cheques.cheque_id",
                deferrable=True,
                initially="IMMEDIATE"
                ),
           primary_key=True,
           unique=True,
    ),
    Column(
        "contract_id",
        Integer,
        ForeignKey(
            "payments_data.contracts.contract_id",
            deferrable=True,
            initially="IMMEDIATE"
            ),
        primary_key=True,
        unique=True,
    ),
    schema="payments_data"
)