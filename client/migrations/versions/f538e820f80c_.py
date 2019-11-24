"""empty message

Revision ID: f538e820f80c
Revises: c5ba17da19f8
Create Date: 2019-11-04 23:34:09.836364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f538e820f80c'
down_revision = 'c5ba17da19f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('updating')
    op.drop_table('server')
    op.drop_index('ix_projects_code', table_name='projects')
    op.drop_index('ix_projects_id', table_name='projects')
    op.drop_table('projects')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('code', sa.VARCHAR(), nullable=True),
    sa.Column('version', sa.VARCHAR(), nullable=True),
    sa.Column('server', sa.VARCHAR(), nullable=True),
    sa.Column('data_path', sa.VARCHAR(), nullable=True),
    sa.Column('config_file_path', sa.VARCHAR(), nullable=True),
    sa.Column('source_code_path', sa.VARCHAR(), nullable=True),
    sa.Column('created_time', sa.VARCHAR(), nullable=True),
    sa.Column('updated_time', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_id', 'projects', ['id'], unique=False)
    op.create_index('ix_projects_code', 'projects', ['code'], unique=1)
    op.create_table('server',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('super_secret', sa.VARCHAR(), nullable=True),
    sa.Column('created_time', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('updating',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('project_id', sa.VARCHAR(), nullable=True),
    sa.Column('project_name', sa.VARCHAR(), nullable=True),
    sa.Column('version', sa.VARCHAR(), nullable=True),
    sa.Column('updating_type', sa.VARCHAR(), nullable=True),
    sa.Column('update_change', sa.VARCHAR(), nullable=True),
    sa.Column('created_time', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    # ### end Alembic commands ###