"""empty message

Revision ID: e11a54c505ab
Revises: af1d748aad5d
Create Date: 2019-03-29 02:26:32.828945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e11a54c505ab'
down_revision = 'af1d748aad5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('payment_amount', sa.Numeric(precision=24, scale=8), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'payment_amount')
    # ### end Alembic commands ###
