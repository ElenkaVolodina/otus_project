"""modify_order_service

Revision ID: 45b76b6e1784
Revises: bd844dcb70b4
Create Date: 2022-12-10 11:08:34.607188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45b76b6e1784'
down_revision = 'bd844dcb70b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('check_hotel', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('check_ticket', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('check_pyment', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'check_pyment')
    op.drop_column('orders', 'check_ticket')
    op.drop_column('orders', 'check_hotel')
    # ### end Alembic commands ###
