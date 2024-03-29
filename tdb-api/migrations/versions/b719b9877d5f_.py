"""empty message

Revision ID: b719b9877d5f
Revises: b47895a08364
Create Date: 2019-04-14 13:40:17.187323

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b719b9877d5f'
down_revision = 'b47895a08364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buy_order',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('side', sa.SmallInteger(), nullable=False),
    sa.Column('number', sa.String(length=16), nullable=False),
    sa.Column('amount', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('details', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('confirm_order',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sell_user_id', sa.String(length=36), nullable=False),
    sa.Column('buy_user_id', sa.String(length=36), nullable=False),
    sa.Column('amount', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['buy_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sell_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match_order',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sell_user_id', sa.String(length=36), nullable=False),
    sa.Column('buy_user_id', sa.String(length=36), nullable=False),
    sa.Column('sell_order_id', sa.Integer(), nullable=False),
    sa.Column('buy_order_id', sa.Integer(), nullable=False),
    sa.Column('sell_number', sa.String(length=16), nullable=False),
    sa.Column('buy_number', sa.String(length=16), nullable=False),
    sa.Column('payment_amount', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('payment_amount_usdt', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('proof_img', sa.Text(), nullable=True),
    sa.Column('current_price', sa.Numeric(precision=24, scale=8), nullable=False),
    sa.Column('payment_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['buy_order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['buy_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.ForeignKeyConstraint(['sell_order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['sell_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('buy_number'),
    sa.UniqueConstraint('sell_number')
    )
    op.create_table('match_order_task',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('assets', sa.Column('community_today_balance', sa.Numeric(precision=24, scale=8), nullable=False))
    op.add_column('order', sa.Column('match_order_id', sa.Integer(), nullable=True))
    op.add_column('order', sa.Column('priority', sa.SmallInteger(), nullable=True))
    op.add_column('order', sa.Column('side', sa.SmallInteger(), nullable=False))
    op.drop_index('number', table_name='order')
    op.create_unique_constraint(None, 'order', ['side', 'number'])
    op.drop_constraint('order_ibfk_3', 'order', type_='foreignkey')
    op.drop_constraint('order_ibfk_1', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'match_order', ['match_order_id'], ['id'])
    op.drop_column('order', 'fee')
    op.drop_column('order', 'payment_id')
    op.drop_column('order', 'match_at')
    op.drop_column('order', 'details')
    op.drop_column('order', 'hold_amount')
    op.drop_column('order', 'current_price')
    op.drop_column('order', 'match_user_id')
    op.drop_column('order', 'proof_img')
    op.drop_column('order', 'payment_amount')
    op.add_column('sell_order', sa.Column('amount', sa.Numeric(precision=24, scale=8), nullable=False))
    op.add_column('sell_order', sa.Column('number', sa.String(length=16), nullable=False))
    op.add_column('sell_order', sa.Column('side', sa.SmallInteger(), nullable=False))
    op.alter_column('sell_order', 'status',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=True)
    op.create_unique_constraint(None, 'sell_order', ['number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sell_order', type_='unique')
    op.alter_column('sell_order', 'status',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=False)
    op.drop_column('sell_order', 'side')
    op.drop_column('sell_order', 'number')
    op.drop_column('sell_order', 'amount')
    op.add_column('order', sa.Column('payment_amount', mysql.DECIMAL(precision=24, scale=8), nullable=False))
    op.add_column('order', sa.Column('proof_img', mysql.TEXT(), nullable=True))
    op.add_column('order', sa.Column('match_user_id', mysql.VARCHAR(length=36), nullable=True))
    op.add_column('order', sa.Column('current_price', mysql.DECIMAL(precision=24, scale=8), nullable=False))
    op.add_column('order', sa.Column('hold_amount', mysql.DECIMAL(precision=24, scale=8), nullable=False))
    op.add_column('order', sa.Column('details', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('order', sa.Column('match_at', mysql.DATETIME(), nullable=True))
    op.add_column('order', sa.Column('payment_id', mysql.VARCHAR(length=36), nullable=True))
    op.add_column('order', sa.Column('fee', mysql.DECIMAL(precision=24, scale=8), nullable=False))
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_ibfk_1', 'order', 'user', ['match_user_id'], ['id'])
    op.create_foreign_key('order_ibfk_3', 'order', 'payment', ['payment_id'], ['id'])
    op.drop_constraint(None, 'order', type_='unique')
    op.create_index('number', 'order', ['number'], unique=True)
    op.drop_column('order', 'side')
    op.drop_column('order', 'priority')
    op.drop_column('order', 'match_order_id')
    op.drop_column('assets', 'community_today_balance')
    op.drop_table('match_order_task')
    op.drop_table('match_order')
    op.drop_table('confirm_order')
    op.drop_table('buy_order')
    # ### end Alembic commands ###
