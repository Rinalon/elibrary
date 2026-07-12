"""change price type in books

Revision ID: 37b00c69d058
Revises: 40a1254965b0
Create Date: 2026-07-11 16:46:53.401962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import MONEY

# revision identifiers, used by Alembic.
revision: str = '37b00c69d058'
down_revision: Union[str, Sequence[str], None] = '40a1254965b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'books',
        sa.Column('price_new', sa.Numeric(10, 2), nullable=True),
        schema='books_data'
    )

    op.execute("""
        UPDATE books_data.books
        SET price_new = CAST(
            replace(
                replace(
                    replace(price::text, ',', ''),
                    '$', ''
                ),
                ' ', ''
            ) AS numeric
        )
        WHERE price_new IS NULL
    """)

    op.alter_column(
        'books',
        'price_new',
        nullable=False,
        schema='books_data'
    )

    op.drop_constraint('books_price_check', 'books', schema='books_data', type_='check')

    op.drop_column('books', 'price', schema='books_data')

    op.alter_column(
        'books',
        'price_new',
        new_column_name='price',
        schema='books_data'
    )

    op.create_check_constraint(
        'books_price_check',
        'books',
        'price >= 0',
        schema='books_data'
    )

    op.alter_column(
        'books',
        'price',
        server_default='0.00',
        schema='books_data'
    )

def downgrade():
    op.drop_constraint('books_price_check', 'books', schema='books_data', type_='check')

    op.add_column(
        'books',
        sa.Column('price_old', MONEY(), nullable=True),
        schema='books_data'
    )

    op.execute("""
        UPDATE books_data.books
        SET price_old = price::money
    """)

    # 4. Удаляем новую колонку
    op.drop_column('books', 'price', schema='books_data')

    op.alter_column(
        'books',
        'price_old',
        new_column_name='price',
        schema='books_data'
    )

    op.alter_column(
        'books',
        'price',
        nullable=False,
        schema='books_data'
    )

    op.create_check_constraint(
        'books_price_check',
        'books',
        'price >= 0::money',
        schema='books_data'
    )