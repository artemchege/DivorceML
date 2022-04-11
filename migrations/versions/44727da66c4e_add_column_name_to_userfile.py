"""add column name to UserFile

Revision ID: 44727da66c4e
Revises: 42945184eb3a
Create Date: 2022-04-10 11:22:12.028791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44727da66c4e'
down_revision = '42945184eb3a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user_file', sa.Column('name', sa.String(), nullable=True))


def downgrade():
    pass
