"""notify-expiry

Revision ID: bd1e892d0609
Revises: 00952c5a4109
Create Date: 2021-07-18 21:26:04.588007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd1e892d0609'
down_revision = '00952c5a4109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('notified_before_expiry', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('requests', sa.Column('notified_expiry', sa.Boolean(), nullable=False, server_default='false'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requests', 'notified_expiry')
    op.drop_column('requests', 'notified_before_expiry')
    # ### end Alembic commands ###
