"""create user roles table

Revision ID: 7b9d596efd3e
Revises: 580f5259d41b
Create Date: 2024-01-29 11:44:44.778321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b9d596efd3e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('user_roles')
    pass
