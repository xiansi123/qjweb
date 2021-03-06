"""empty message

Revision ID: 0e1f77032dcf
Revises: b81fbfc76498
Create Date: 2018-05-27 16:51:09.159820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e1f77032dcf'
down_revision = 'b81fbfc76498'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dynamic', sa.Column('Dynamic_content', sa.Text(), nullable=True))
    op.add_column('dynamic', sa.Column('Dynamic_name', sa.String(length=30), nullable=True))
    op.add_column('dynamic', sa.Column('Dynamic_time', sa.String(length=30), nullable=True))
    op.add_column('dynamic', sa.Column('Dynamic_type', sa.String(length=10), nullable=True))
    op.add_column('dynamic', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dynamic', 'create_time')
    op.drop_column('dynamic', 'Dynamic_type')
    op.drop_column('dynamic', 'Dynamic_time')
    op.drop_column('dynamic', 'Dynamic_name')
    op.drop_column('dynamic', 'Dynamic_content')
    # ### end Alembic commands ###
