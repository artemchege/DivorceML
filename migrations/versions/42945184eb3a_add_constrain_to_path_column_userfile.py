"""add constrain to path column UserFile

Revision ID: 42945184eb3a
Revises: 7bee92ff861b
Create Date: 2022-04-09 16:59:19.947892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42945184eb3a'
down_revision = '7bee92ff861b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('path_unique_constrain', 'user_file', ['path'])


def downgrade():
    pass
