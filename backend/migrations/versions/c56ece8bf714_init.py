"""init

Revision ID: c56ece8bf714
Revises: 
Create Date: 2022-05-07 08:59:08.594134

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision = 'c56ece8bf714'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_age'), 'user', ['age'], unique=False)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_hashed_password'), 'user', ['hashed_password'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_is_superuser'), 'user', ['is_superuser'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('note',
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_note_completed'), 'note', ['completed'], unique=False)
    op.create_index(op.f('ix_note_created_at'), 'note', ['created_at'], unique=False)
    op.create_index(op.f('ix_note_id'), 'note', ['id'], unique=False)
    op.create_index(op.f('ix_note_owner_id'), 'note', ['owner_id'], unique=False)
    op.create_index(op.f('ix_note_text'), 'note', ['text'], unique=False)
    op.create_index(op.f('ix_note_updated_at'), 'note', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_note_updated_at'), table_name='note')
    op.drop_index(op.f('ix_note_text'), table_name='note')
    op.drop_index(op.f('ix_note_owner_id'), table_name='note')
    op.drop_index(op.f('ix_note_id'), table_name='note')
    op.drop_index(op.f('ix_note_created_at'), table_name='note')
    op.drop_index(op.f('ix_note_completed'), table_name='note')
    op.drop_table('note')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_is_superuser'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_hashed_password'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_age'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###