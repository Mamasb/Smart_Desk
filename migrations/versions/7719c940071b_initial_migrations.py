"""initial migrations

Revision ID: 7719c940071b
Revises: 
Create Date: 2025-01-24 10:08:19.230793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7719c940071b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admission_number', sa.String(length=10), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=True),
    sa.Column('family_name', sa.String(length=50), nullable=False),
    sa.Column('grade', sa.String(length=20), nullable=False),
    sa.Column('food', sa.Boolean(), nullable=True),
    sa.Column('text_books_fee', sa.Boolean(), nullable=True),
    sa.Column('exercise_books_fee', sa.String(length=10), nullable=True),
    sa.Column('assesment_tool_fee', sa.Boolean(), nullable=True),
    sa.Column('transport_mode', sa.String(length=20), nullable=True),
    sa.Column('transport_fee', sa.Float(), nullable=True),
    sa.Column('total_fee', sa.Float(), nullable=True),
    sa.Column('fees_paid', sa.Float(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('admission_number')
    )
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('amount_due', sa.Float(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('paid_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoices')
    op.drop_table('student')
    # ### end Alembic commands ###
