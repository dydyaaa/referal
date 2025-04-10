"""add sets model

Revision ID: d0e3efe98522
Revises: ab82379adb45
Create Date: 2025-03-26 12:51:16.150748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0e3efe98522'
down_revision = 'ab82379adb45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.drop_column('weight')
        batch_op.drop_column('sets')
        batch_op.drop_column('reps')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reps', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('sets', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
