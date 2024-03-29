"""empty message

Revision ID: 86dc8c497244
Revises: 8444b9ec6e5a
Create Date: 2024-01-27 12:18:43.785472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '86dc8c497244'
down_revision: Union[str, None] = '8444b9ec6e5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts_inst',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session_file_path', sa.String(), nullable=False),
    sa.Column('target_channel', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accounts_tg',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session_file_path', sa.String(), nullable=False),
    sa.Column('target_chat', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('advertising_channels', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=False),
    sa.Column('account_tg_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_tg_id'], ['accounts_tg.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('account_inst_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_inst_id'], ['accounts_inst.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_chat_members',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_premium', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name='telegram_chat_members_account_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='telegram_chat_members_pkey')
    )
    op.create_table('accounts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('session_file_path', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('target_chat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('advertising_channels', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='accounts_pkey')
    )
    op.drop_table('followers')
    op.drop_table('chat_members')
    op.drop_table('accounts_tg')
    op.drop_table('accounts_inst')
    # ### end Alembic commands ###
