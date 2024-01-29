"""create tickets table

Revision ID: 2bd28a818aed
Revises: 580f5259d41b
Create Date: 2024-01-29 11:52:14.610699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bd28a818aed'
down_revision: Union[str, None] = '580f5259d41b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tickets',
        sa.column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.column('company_name', sa.String(), nullable=False),
        sa.column('contact_person', sa.String(), nullable=False, unique=True, index=True),
        sa.column('application', sa.String(), nullable=False ),
        sa.column('version', sa.String() ),
        sa.column('start_date', sa.DateTime(), nullable=False, default=datetime.datetime.now().date() ),
        sa.Column('start_time', sa.DateTime(), nullable=False, default=datetime.datetime.now().time()),
        sa.column('end_date', sa.DateTime(), nullable=False, default=datetime.datetime.now().date()),
        sa.column('end_time', sa.DateTime(), nullable=False, default=datetime.datetime.now().time()),
        sa.column('problem_reported', sa.String(), nullable=False),
        sa.column('diagnosis', sa.String(), nullable=False),
        sa.column('solution_provided', sa.String(), nullable=False),
        sa.column('total_hrs', sa.Numeric(), nullable=False),
        sa.column('amount', sa.Float(), nullable=False),
        sa.column('chargeable', sa.Boolean(), default=False, nullable=False),
        sa.column('consultant_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),

        op.create_foreign_key('fk_tickets_user', source_table="tickets", referent_table="users",
        local_cols=['consultant_id'], remote_cols=['id'], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_table('tickets')
    pass
