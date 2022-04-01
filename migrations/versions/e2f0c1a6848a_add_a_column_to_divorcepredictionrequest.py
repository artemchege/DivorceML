"""add a column to DivorcePredictionRequest

Revision ID: e2f0c1a6848a
Revises: f327cd3f47ff
Create Date: 2022-04-01 18:14:39.629753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f0c1a6848a'
down_revision = 'f327cd3f47ff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('divorce_prediction_request', sa.Column('prediction', sa.Float()))


def downgrade():
    pass
