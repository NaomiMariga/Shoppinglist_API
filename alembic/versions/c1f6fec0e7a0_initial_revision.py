"""initial revision

Revision ID: c1f6fec0e7a0
Revises: 
Create Date: 2017-11-20 21:09:28.030674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f6fec0e7a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.BigInteger, primary_key=True),
        sa.column('email', sa.String(100), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('pword', sa.String(64), nullable=False),
        sa.column('date_registered', sa.TIMESTAMP, default=sa.func.now())

    )
    op.create_table(
        'lists',
        sa.Column('list_id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('list_name', sa.String(50), nullable=False),
        sa.Column('time_updated', sa.TIMESTAMP, default=sa.func.now())
    )

    op.create_table(
        'items',
        sa.Column('item_id', sa.BigInteger, primary_key=True),
        sa.Column('list_id', sa.Integer),
        sa.Column('item_name', sa.String(50), nullable=False),
        sa.Column('quantity', sa.Float),
        sa.Column('units', sa.String(5)),
        sa.Column('item_cost', sa.Float),
        sa.Column('time_updated', sa.TIMESTAMP, default=sa.func.now())

    )
    op.create_table(
        'authentication',
        sa.Column('auth_id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('auth_token', sa.String(100)),
        sa.Column('login_time', sa.TIMESTAMP, default=sa.func.now())

    )
    op.create_foreign_key(
        'user_id',
        'users', 'authentication',
        ['user_id'], ['user_id']
    )
    op.create_foreign_key(
        'list_id',
        'lists',
        ['list_id']
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('lists')
    op.drop_table('items')
    op.drop_table('authentication')
    op.drop_foreign_key('user_id')
    op.drop_foreign_key('list_id')
