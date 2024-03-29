"""empty message

Revision ID: edb3efaf8435
Revises: 74ead3e69b34
Create Date: 2019-03-11 01:08:52.212288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edb3efaf8435'
down_revision = '74ead3e69b34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crypto_currency',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency_code', sa.String(length=20), nullable=False),
    sa.Column('erc20_token', sa.SmallInteger(), nullable=False),
    sa.Column('usd_price', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('sequence', sa.SmallInteger(), nullable=False),
    sa.Column('init_block_number', sa.Integer(), nullable=False),
    sa.Column('indexed_block_number', sa.Integer(), nullable=False),
    sa.Column('start_price', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('percent_change_1h', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('percent_change_24h', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('percent_change_7d', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('currency_code', 'erc20_token')
    )
    op.create_table('fiat_currency',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=60), nullable=False),
    sa.Column('country_code', sa.String(length=20), nullable=False),
    sa.Column('currency', sa.String(length=60), nullable=False),
    sa.Column('currency_code', sa.String(length=20), nullable=False),
    sa.Column('usd_rate', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('sequence', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country_code', 'currency_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fiat_currency')
    op.drop_table('crypto_currency')
    # ### end Alembic commands ###
