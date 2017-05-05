"""empty message

Revision ID: fe159ce13e78
Revises: 3f146b49b509
Create Date: 2017-05-05 11:45:54.123882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe159ce13e78'
down_revision = '3f146b49b509'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=255), nullable=True),
    sa.Column('action', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audit')
    # ### end Alembic commands ###
