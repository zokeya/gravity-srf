"""create_posts_table

Revision ID: 6d34d59ba747
Revises: 2bd28a818aed
Create Date: 2024-01-26 16:17:18.615240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision: str = '6d34d59ba747'
down_revision: Union[str, None] = '2bd28a818aed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        op.create_foreign_key('fk_post_users', source_table="posts", referent_table="users",
        local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
