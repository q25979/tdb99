"""empty message

Revision ID: 7d67ad515967
Revises: 6d35caa63912
Create Date: 2019-03-09 15:08:35.563179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d67ad515967'
down_revision = '6d35caa63912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recommend_schedule_task',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('processed_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.add_column('user', sa.Column('received_reward', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('state', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'state')
    op.drop_column('user', 'received_reward')
    op.drop_table('recommend_schedule_task')
    # ### end Alembic commands ###
