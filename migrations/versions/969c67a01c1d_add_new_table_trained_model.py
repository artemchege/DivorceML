"""add new table trained_model

Revision ID: 969c67a01c1d
Revises: 44727da66c4e
Create Date: 2022-04-12 21:36:18.599898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '969c67a01c1d'
down_revision = '44727da66c4e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('trained_model',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('accuracy', sa.Float(), nullable=False),
                    sa.Column('precision', sa.Float(), nullable=False),
                    sa.Column('recall', sa.Float(), nullable=False),
                    sa.Column('path', sa.String(), nullable=False, unique=True),
                    sa.Column('user_file_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_file_id'], ['user_file.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade():
    pass
