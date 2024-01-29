"""create users table

Revision ID: 580f5259d41b
Revises: 6d34d59ba747
Create Date: 2024-01-26 16:46:13.781783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '580f5259d41b'
down_revision: Union[str, None] = '7b9d596efd3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.column('name', sa.String(), nullable=False),
        sa.column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.column('password', sa.String(), nullable=False ),
        sa.column('signature_url', sa.String() ),
        sa.column('image_url', sa.String() ),
        sa.Column('user_role_id', sa.Integer(), nullable=False),
        sa.column('is_active', sa.Boolean(), default=False, nullable=False),

        op.create_foreign_key('fk_users_roles', source_table="users", referent_table="user_roles",
        local_cols=['user_role_id'], remote_cols=['id'], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
