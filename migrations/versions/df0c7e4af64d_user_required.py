"""user required

Revision ID: df0c7e4af64d
Revises: cfac105b681c
Create Date: 2022-03-23 20:00:54.563229

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'df0c7e4af64d'
down_revision = 'cfac105b681c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_divorce_prediction_request_id', table_name='divorce_prediction_request')
    # op.drop_table('divorce_prediction_request')
    # op.drop_index('ix_user_id', table_name='user')
    # op.drop_table('user')
    op.alter_column('divorce_prediction_request', 'user_id', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_table('divorce_prediction_request',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('hate_subject', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('happy', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dreams', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('freedom_value', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('likes', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('calm_breaks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('harmony', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('roles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('inner_world', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('current_stress', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('friends_social', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('contact', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('insult', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='divorce_prediction_request_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='divorce_prediction_request_pkey')
    )
    op.create_index('ix_divorce_prediction_request_id', 'divorce_prediction_request', ['id'], unique=False)
    # ### end Alembic commands ###
