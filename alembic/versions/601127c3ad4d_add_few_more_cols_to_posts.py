"""add few more cols to post

Revision ID: 601127c3ad4d
Revises: 8768b7d20cab
Create Date: 2025-08-21 21:39:15.428679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '601127c3ad4d'
down_revision: Union[str, Sequence[str], None] = '8768b7d20cab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'post',
        sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE'))
    )
    op.add_column(
        'post',
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False,
                  server_default=sa.text('now()'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'post', 'created_at'
    )
    op.drop_column(
        'post','published'
    )
