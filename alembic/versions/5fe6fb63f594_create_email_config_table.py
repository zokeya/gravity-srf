"""create email config table

Revision ID: 5fe6fb63f594
Revises: 6d34d59ba747
Create Date: 2024-01-29 12:18:07.345524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fe6fb63f594'
down_revision: Union[str, None] = '6d34d59ba747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'email_config',
        sa.column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('smtp_server', sa.StrStringing(), index=True),
        sa.Column('smtp_port', sa.Integer(), nullable=False),
        sa.Column('smtp_username', sa.String(), nullable=False),
        sa.Column('smtp_password', sa.String(), nullable=False),
        sa.Column('sender_email', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True)
    )
    pass


def downgrade() -> None:
    op.drop_table('email_config')
    pass
