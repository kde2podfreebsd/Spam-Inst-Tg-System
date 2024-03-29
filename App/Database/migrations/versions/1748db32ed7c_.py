"""empty message

Revision ID: 1748db32ed7c
Revises: 86dc8c497244
Create Date: 2024-01-31 00:06:03.655013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1748db32ed7c'
down_revision: Union[str, None] = '86dc8c497244'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('target_channels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('accounts_inst', sa.Column('status', sa.Boolean(), nullable=False))
    op.add_column('chat_members', sa.Column('target_channel_id', sa.Integer(), nullable=True))
    op.drop_constraint('chat_members_account_tg_id_fkey', 'chat_members', type_='foreignkey')
    op.create_foreign_key(None, 'chat_members', 'target_channels', ['target_channel_id'], ['id'])
    op.drop_column('chat_members', 'account_tg_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_members', sa.Column('account_tg_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'chat_members', type_='foreignkey')
    op.create_foreign_key('chat_members_account_tg_id_fkey', 'chat_members', 'accounts_tg', ['account_tg_id'], ['id'])
    op.drop_column('chat_members', 'target_channel_id')
    op.drop_column('accounts_inst', 'status')
    op.drop_table('target_channels')
    # ### end Alembic commands ###
