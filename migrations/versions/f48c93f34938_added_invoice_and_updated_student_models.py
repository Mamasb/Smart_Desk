"""Added Invoice and updated Student models

Revision ID: f48c93f34938
Revises: d60fa44f613f
Create Date: 2025-01-03 17:41:11.355559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f48c93f34938'
down_revision = 'd60fa44f613f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount_paid', sa.Float(), nullable=True))
        batch_op.drop_column('fees_paid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fees_paid', mysql.FLOAT(), server_default=sa.text('0'), nullable=True))
        batch_op.drop_column('amount_paid')

    # ### end Alembic commands ###
