"""create emails table

Revision ID: 711871045e6e
Revises: 5fe6fb63f594
Create Date: 2024-01-29 12:17:57.781376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '711871045e6e'
down_revision: Union[str, None] = '5fe6fb63f594'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'emails',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('to_email', sa.String(), index=True),
        sa.Column('subject', sa.String(), nullable=False),
        sa.Column('body', sa.Text()),
        sa.Column('is_sent', sa.Boolean(), default=False),
        sa.Column('error_details', sa.String()),
        sa.Column('sent_date', sa.DateTime(timezone=False), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    pass


def downgrade() -> None:
    op.drop_table('emails')
    pass
