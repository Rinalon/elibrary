"""change rating type  in books_data.reviews

Revision ID: 40a1254965b0
Revises: 986e458bbacb
Create Date: 2026-07-08 15:55:53.527544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a1254965b0'
down_revision: Union[str, Sequence[str], None] = '986e458bbacb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'reviews',
        'rating',
        type_=sa.SmallInteger,
        schema='books_data',
    )

    op.drop_constraint(
        "reviews_rating_check",
        "reviews",
        schema='books_data'
    )

    op.create_check_constraint(
        "reviews_rating_check",
        "reviews",
        condition="rating >= 0 AND rating <= 5",
        schema='books_data'
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
