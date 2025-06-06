"""add cart model

Revision ID: ed971b229bb6
Revises: 8a01f87fe48c
Create Date: 2025-05-26 11:07:27.596407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed971b229bb6'
down_revision: Union[str, None] = '8a01f87fe48c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('price', sa.Integer(), nullable=False))
    op.add_column('orders', sa.Column('created_ad', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'created_ad')
    op.drop_column('order_items', 'price')
    # ### end Alembic commands ###
