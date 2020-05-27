"""empty message

Revision ID: 69aed37271bd
Revises: 8c9504ff885b
Create Date: 2020-05-19 13:55:55.103497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69aed37271bd'
down_revision = '8c9504ff885b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock__highlow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_name', sa.String(length=6), nullable=True),
    sa.Column('high_val52wk', sa.Numeric(), nullable=True),
    sa.Column('low_val52wk', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock__image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_name', sa.String(length=6), nullable=True),
    sa.Column('image_url', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=6), nullable=True),
    sa.Column('company_name', sa.String(length=500), nullable=True),
    sa.Column('open', sa.Numeric(), nullable=True),
    sa.Column('lastest_price', sa.Numeric(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    op.drop_table('stock__image')
    op.drop_table('stock__highlow')
    # ### end Alembic commands ###