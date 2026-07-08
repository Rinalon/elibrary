"""added birthdate to personal_data

Revision ID: e01339e0598b
Revises: 0c62eed68245
Create Date: 2026-07-08 13:26:12.889730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e01339e0598b'
down_revision: Union[str, Sequence[str], None] = '0c62eed68245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

   op.add_column(
       "personal_data",
        sa.Column("birthdate", sa.DateTime),
        schema="clients",
   )


def downgrade() -> None:
    pass