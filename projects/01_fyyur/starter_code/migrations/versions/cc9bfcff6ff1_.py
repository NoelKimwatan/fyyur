"""empty message

Revision ID: cc9bfcff6ff1
Revises: 563f9a439d0e
Create Date: 2022-08-14 13:22:06.106276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc9bfcff6ff1'
down_revision = '563f9a439d0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'image_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
