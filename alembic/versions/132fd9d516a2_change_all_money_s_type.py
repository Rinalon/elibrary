"""change all money's type

Revision ID: 132fd9d516a2
Revises: 37b00c69d058
Create Date: 2026-07-11 17:20:57.004155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import MONEY

# revision identifiers, used by Alembic.
revision: str = '132fd9d516a2'
down_revision: Union[str, Sequence[str], None] = '37b00c69d058'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.drop_constraint('subscribe_types_price_check', 'subscribe_types', schema='subscribes_data', type_='check')

    op.alter_column(
        'subscribe_types',
        'price',
        schema='subscribes_data',
        existing_type=MONEY(),
        type_=sa.Numeric(),
        postgresql_using='price::numeric',
        nullable=False,
        server_default='0'
    )
    # Создаём новый CHECK
    op.create_check_constraint(
        'subscribe_types_price_check',
        'subscribe_types',
        'price >= 0',
        schema='subscribes_data'
    )

    # 2. Чеки (cheques)
    op.drop_constraint('cheques_total_cost_check', 'cheques', schema='payments_data', type_='check')
    op.alter_column(
        'cheques',
        'total_cost',
        schema='payments_data',
        existing_type=MONEY(),
        type_=sa.Numeric(),
        postgresql_using='total_cost::numeric',
        nullable=False
    )
    op.create_check_constraint(
        'cheques_total_cost_check',
        'cheques',
        'total_cost >= 0',
        schema='payments_data'
    )

    op.drop_constraint('contracts_total_cost_check', 'contracts', schema='payments_data', type_='check')
    op.alter_column(
        'contracts',
        'total_cost',
        schema='payments_data',
        existing_type=MONEY(),
        type_=sa.Numeric(),
        postgresql_using='total_cost::numeric',
        nullable=False
    )
    op.create_check_constraint(
        'contracts_total_cost_check',
        'contracts',
        'total_cost >= 0',
        schema='payments_data'
    )


def downgrade():
    op.drop_constraint('subscribe_types_price_check', 'subscribe_types', schema='subscribes_data', type_='check')
    op.drop_constraint('cheques_total_cost_check', 'cheques', schema='payments_data', type_='check')
    op.drop_constraint('contracts_total_cost_check', 'contracts', schema='payments_data', type_='check')

    op.alter_column(
        'subscribe_types',
        'price',
        schema='subscribes_data',
        existing_type=sa.Numeric(),
        type_=MONEY(),
        postgresql_using='price::money',
        nullable=False,
        server_default='0'
    )
    op.alter_column(
        'cheques',
        'total_cost',
        schema='payments_data',
        existing_type=sa.Numeric(),
        type_=MONEY(),
        postgresql_using='total_cost::money',
        nullable=False
    )
    op.alter_column(
        'contracts',
        'total_cost',
        schema='payments_data',
        existing_type=sa.Numeric(),
        type_=MONEY(),
        postgresql_using='total_cost::money',
        nullable=False
    )

    # Восстанавливаем старые CHECK
    op.create_check_constraint(
        'subscribe_types_price_check',
        'subscribe_types',
        'price >= 0::money',
        schema='subscribes_data'
    )
    op.create_check_constraint(
        'cheques_total_cost_check',
        'cheques',
        'total_cost >= 0::money',
        schema='payments_data'
    )
    op.create_check_constraint(
        'contracts_total_cost_check',
        'contracts',
        'total_cost >= 0::money',
        schema='payments_data'
    )