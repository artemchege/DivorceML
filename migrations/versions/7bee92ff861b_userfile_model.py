"""UserFile model

Revision ID: 7bee92ff861b
Revises: e2f0c1a6848a
Create Date: 2022-04-09 16:14:51.232957

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7bee92ff861b'
down_revision = 'e2f0c1a6848a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_file',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('path', sa.String(), nullable=False, unique=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade():
    pass
