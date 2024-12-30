"""Set default value for fees_paid and other financial fields

Revision ID: 7e360aa67eac
Revises: 
Create Date: 2024-12-30 15:35:10.524528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# Revision identifiers, used by Alembic.
revision = '7e360aa67eac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ensure invalid or NULL values in `fees_paid` are corrected before altering
    op.execute(
        """
        UPDATE student 
        SET fees_paid = 0.0 
        WHERE fees_paid IS NULL OR fees_paid NOT REGEXP '^[0-9]+(\\.[0-9]+)?$';
        """
    )

    # Alter `fees_paid` column to set NOT NULL and default value
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column(
            'fees_paid',
            existing_type=mysql.FLOAT(),
            nullable=False,
            server_default=sa.text("0.0")
        )

    # Alter `exercise_books_fee` column to use String(10)
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column(
            'exercise_books_fee',
            existing_type=mysql.TINYINT(display_width=1),
            type_=sa.String(length=10),
            nullable=True
        )
    
    # Add or ensure unique constraint for `admission_number`
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_admission_number', ['admission_number'])


def downgrade():
    # Revert changes to `fees_paid` column
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column(
            'fees_paid',
            existing_type=mysql.FLOAT(),
            nullable=True,
            server_default=None
        )

    # Revert `exercise_books_fee` column back to TINYINT
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column(
            'exercise_books_fee',
            existing_type=sa.String(length=10),
            type_=mysql.TINYINT(display_width=1),
            nullable=True
        )

    # Remove the unique constraint for `admission_number`
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint('uq_admission_number', type_='unique')
