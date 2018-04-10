"""empty message

Revision ID: 285d3767151d
Revises: 21205c8072a3
Create Date: 2018-04-08 18:13:37.240935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '285d3767151d'
down_revision = '21205c8072a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tea', sa.Column('others', sa.Text(), nullable=True))
    op.alter_column('tea', 'no',
               existing_type=mysql.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tea', 'no',
               existing_type=mysql.VARCHAR(length=16),
               nullable=False)
    op.drop_column('tea', 'others')
    # ### end Alembic commands ###
