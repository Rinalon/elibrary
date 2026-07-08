"""added limitations for birthdate

Revision ID: 986e458bbacb
Revises: 97a4ddff7ef6
Create Date: 2026-07-08 13:40:16.512650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '986e458bbacb'
down_revision: Union[str, Sequence[str], None] = '97a4ddff7ef6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "personal_data",
        "birthdate",
        nullable=False,
        schema="clients"
    )

    op.create_check_constraint(
        "ck_personal_data_birthdate_check",
        "personal_data",
    "birthdate BETWEEN '1900-01-01'::date AND CURRENT_DATE",
        schema='clients'
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
