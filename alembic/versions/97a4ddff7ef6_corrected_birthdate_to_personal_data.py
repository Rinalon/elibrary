"""corrected birthdate to personal_data

Revision ID: 97a4ddff7ef6
Revises: e01339e0598b
Create Date: 2026-07-08 13:37:15.924720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97a4ddff7ef6'
down_revision: Union[str, Sequence[str], None] = 'e01339e0598b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'personal_data',
        'birthdate',
        type_=sa.Date,
        schema='clients'
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
