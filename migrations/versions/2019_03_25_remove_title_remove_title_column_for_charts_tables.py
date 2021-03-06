"""Remove title column for charts/tables

Revision ID: 2019_03_25_remove_title
Revises: 2019_03_21_add_titles
Create Date: 2019-03-25 13:17:19.385632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2019_03_25_remove_title"
down_revision = "2019_03_21_add_titles"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("dimension_chart", "title")
    op.drop_column("dimension_table", "title")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("dimension_table", sa.Column("title", sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column("dimension_chart", sa.Column("title", sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
