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
        sa.Column('email', sa.String(100)),
        sa.Column('username', sa.String(50)),
        sa.Column('pword', sa.String(64)),
        sa.Column('date_registered', sa.DateTime)
    )
    op.create_table(
        'lists',
        sa.Column('list_id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('list_name', sa.String(50)),
        sa.Column('time_updated', sa.DateTime, server_default=sa.func.current_timestamp())
    )

    op.create_table(
        'items',
        sa.Column('item_id', sa.BigInteger, primary_key=True),
        sa.Column('list_id', sa.Integer),
        sa.Column('item_name', sa.String(50)),
        sa.Column('quantity', sa.Float),
        sa.Column('units', sa.String(5)),
        sa.Column('item_cost', sa.Float),
        sa.Column('time_updated', sa.DateTime, server_default=sa.func.current_timestamp())

    )
    op.create_table(
        'authentication',
        sa.Column('auth_id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('auth_token', sa.String(100)),
        sa.Column('login_time', sa.DateTime, server_default=sa.func.current_timestamp())

    )
    op.create_foreign_key(
        'fk_lists_user_id',
        'lists', 'users',
        ['user_id'], ['user_id'],
    )
    op.create_foreign_key(
        'fk_authentication_user_id',
        'authentication', 'users',
        ['user_id'], ['user_id']
    )
    op.create_foreign_key(
        'fk_items_list_id',
        'items', 'lists',
        ['list_id'], ['list_id'],
    )


def downgrade():
    op.drop_table('authentication')
    op.drop_table('items')
    op.drop_table('lists')
    op.drop_table('users')



