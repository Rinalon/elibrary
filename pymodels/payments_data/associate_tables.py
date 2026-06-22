from sqlalchemy import Table, Column, Integer, ForeignKey
from pymodels.base import Base

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
           primary_key=True
    ),
    Column(
        "contract_id",
        Integer,
        ForeignKey(
            "payments_data.contracts.contract_id",
            deferrable=True,
            initially="IMMEDIATE"
            ),
        primary_key=True
    ),
    schema="payments_data"
)