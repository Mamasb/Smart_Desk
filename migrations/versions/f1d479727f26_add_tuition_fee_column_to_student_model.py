"""Add tuition_fee column to Student model

Revision ID: f1d479727f26
Revises: 6fd1389036a0
Create Date: 2025-01-08 18:06:08.283623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f1d479727f26'
down_revision = '6fd1389036a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assesment_tool_fee', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('transport_fee', sa.Float(), nullable=True))
        batch_op.alter_column('food',
               existing_type=mysql.FLOAT(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('text_books_fee',
               existing_type=mysql.FLOAT(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('exercise_books_fee',
               existing_type=mysql.FLOAT(),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('transport_mode',
               existing_type=mysql.FLOAT(),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.drop_column('assessment_tool_fee')
        batch_op.drop_column('activity_fee')
        batch_op.drop_column('school_diary_fee')
        batch_op.drop_column('tuition_fee')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tuition_fee', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('school_diary_fee', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('activity_fee', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('assessment_tool_fee', mysql.FLOAT(), nullable=True))
        batch_op.alter_column('transport_mode',
               existing_type=sa.String(length=20),
               type_=mysql.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('exercise_books_fee',
               existing_type=sa.String(length=10),
               type_=mysql.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('text_books_fee',
               existing_type=sa.Boolean(),
               type_=mysql.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('food',
               existing_type=sa.Boolean(),
               type_=mysql.FLOAT(),
               existing_nullable=True)
        batch_op.drop_column('transport_fee')
        batch_op.drop_column('assesment_tool_fee')

    # ### end Alembic commands ###
