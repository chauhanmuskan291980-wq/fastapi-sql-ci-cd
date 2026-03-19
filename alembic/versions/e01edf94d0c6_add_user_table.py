"""add user table

Revision ID: e01edf94d0c6
Revises: 75fb22cef385
Create Date: 2026-03-19 14:43:32.789187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e01edf94d0c6'
down_revision: Union[str, Sequence[str], None] = '75fb22cef385'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
 

def upgrade():

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table(
        'newpost',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    )

    op.create_table(
        'vote',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('newpost.id', ondelete='CASCADE'), primary_key=True)
    )


def downgrade():
    op.drop_table('vote')
    op.drop_table('newpost')
    op.drop_table('users')