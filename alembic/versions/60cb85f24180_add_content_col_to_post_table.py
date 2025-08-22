"""add content col to post table

Revision ID: 60cb85f24180
Revises: 75391d4d5f7f
Create Date: 2025-08-21 21:14:48.062281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60cb85f24180'
down_revision: Union[str, Sequence[str], None] = '75391d4d5f7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'post',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post','content')
