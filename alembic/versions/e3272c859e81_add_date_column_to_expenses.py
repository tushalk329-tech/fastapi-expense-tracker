"""add date column to expenses

Revision ID: e3272c859e81
Revises: 
Create Date: 2026-04-01 00:22:42.739055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3272c859e81'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('date', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
