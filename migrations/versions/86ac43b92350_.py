"""empty message

Revision ID: 86ac43b92350
Revises: 
Create Date: 2020-05-17 16:46:53.557398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86ac43b92350'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('p_type', sa.String(length=200), nullable=True),
    sa.Column('holding', sa.String(length=5), nullable=True),
    sa.Column('holding_long', sa.String(length=250), nullable=True),
    sa.Column('shares', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('change', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restriction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('financial', sa.Boolean(), nullable=True),
    sa.Column('utilitie', sa.Boolean(), nullable=True),
    sa.Column('health_care', sa.Boolean(), nullable=True),
    sa.Column('con_dis', sa.Boolean(), nullable=True),
    sa.Column('energy', sa.Boolean(), nullable=True),
    sa.Column('industrials', sa.Boolean(), nullable=True),
    sa.Column('con_staples', sa.Boolean(), nullable=True),
    sa.Column('re', sa.Boolean(), nullable=True),
    sa.Column('tech', sa.Boolean(), nullable=True),
    sa.Column('materials', sa.Boolean(), nullable=True),
    sa.Column('telco', sa.Boolean(), nullable=True),
    sa.Column('etf', sa.Boolean(), nullable=True),
    sa.Column('restricted', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('risk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('initial', sa.Numeric(precision=0, asdecimal=False), nullable=True),
    sa.Column('target', sa.Numeric(), nullable=True),
    sa.Column('tolerance', sa.Numeric(), nullable=True),
    sa.Column('priority', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strategy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('growth', sa.Boolean(), nullable=True),
    sa.Column('value', sa.Boolean(), nullable=True),
    sa.Column('none', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('structure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('us_equities', sa.Boolean(), nullable=True),
    sa.Column('us_bonds', sa.Boolean(), nullable=True),
    sa.Column('treasury', sa.Boolean(), nullable=True),
    sa.Column('int_equities', sa.Boolean(), nullable=True),
    sa.Column('commodities', sa.Boolean(), nullable=True),
    sa.Column('real_estate', sa.Boolean(), nullable=True),
    sa.Column('mlps', sa.Boolean(), nullable=True),
    sa.Column('int_bonds', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('structure')
    op.drop_table('strategy')
    op.drop_table('risk')
    op.drop_table('restriction')
    op.drop_table('portfolio')
    # ### end Alembic commands ###
