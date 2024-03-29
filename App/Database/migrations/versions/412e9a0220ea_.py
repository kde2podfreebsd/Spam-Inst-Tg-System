"""empty message

Revision ID: 412e9a0220ea
Revises: 1748db32ed7c
Create Date: 2024-01-31 13:43:54.430335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '412e9a0220ea'
down_revision: Union[str, None] = '1748db32ed7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_members')
    op.add_column('target_channels', sa.Column('premium_members', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('target_channels', 'premium_members')
    op.create_table('chat_members',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_premium', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('target_channel_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['target_channel_id'], ['target_channels.id'], name='chat_members_target_channel_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='chat_members_pkey')
    )
    # ### end Alembic commands ###
