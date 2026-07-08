"""added birthdate to personal_data

Revision ID: 0c62eed68245
Revises: 8298195cb51e
Create Date: 2026-07-08 13:17:48.199619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0c62eed68245'
down_revision: Union[str, Sequence[str], None] = '8298195cb51e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

   op.add_column(
       "personal_data",
        sa.Column("birthdate", sa.DateTime, nullable=False),
        schema="clients",
   )


def downgrade() -> None:
    pass