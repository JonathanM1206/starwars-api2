"""empty message

Revision ID: 76fb62ee1d26
Revises: 0bb8ba29f932
Create Date: 2025-02-19 18:30:05.393884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76fb62ee1d26'
down_revision = '0bb8ba29f932'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_name', sa.String(length=15), nullable=False),
    sa.Column('planet_climate', sa.String(length=15), nullable=False),
    sa.Column('planet_residents', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet')
    # ### end Alembic commands ###
