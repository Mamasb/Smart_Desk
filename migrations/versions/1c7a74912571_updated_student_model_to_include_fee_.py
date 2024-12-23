"""Updated Student model to include fee calculation

Revision ID: 1c7a74912571
Revises: 90e3e736e6f5
Create Date: 2024-12-11 16:02:29.105461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c7a74912571'
down_revision = '90e3e736e6f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fees_paid', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('fees_paid')

    # ### end Alembic commands ###
