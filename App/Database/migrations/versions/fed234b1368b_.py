"""empty message

Revision ID: fed234b1368b
Revises: b9cdb39ff343
Create Date: 2024-02-04 16:37:32.726182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed234b1368b'
down_revision: Union[str, None] = 'b9cdb39ff343'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('premium_chat_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('account_stories_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_stories_id'], ['accounts_stories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('premium_chat_members')
    # ### end Alembic commands ###
