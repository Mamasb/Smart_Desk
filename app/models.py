from . import db
from datetime import timedelta

# Invoice model to represent the invoice for a student
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # Correct ForeignKey
    amount_due = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid_date = db.Column(db.Date, nullable=True)

    # Relationship with Student (back_populates for explicit linkage)
    student = db.relationship('Student', back_populates='invoices')

    def __repr__(self):
        return f"<Invoice {self.id} for {self.student.first_name} {self.student.family_name}>"

# Student model to represent a student record
class Student(db.Model):
    __tablename__ = "student"  # Keep the table name as 'student' to avoid affecting existing data

    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(10), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    family_name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(20), nullable=False)

    # Optional fees
    food = db.Column(db.Boolean, default=False)
    text_books_fee = db.Column(db.Boolean, default=False)
    exercise_books_fee = db.Column(db.Boolean, default=False)
    assesment_tool_fee = db.Column(db.Boolean, default=False)
    transport_mode = db.Column(db.String(20), nullable=True)  # e.g., 'OneWay', 'TwoWayTown'
    transport_fee = db.Column(db.Float, default=0.0)
    total_fee = db.Column(db.Float, default=0.0)

    # Fees paid will be updated later from bank statements
    fees_paid = db.Column(db.Float, default=0.0)  # Placeholder for fees paid from bank statement

    # New balance column to track balance
    balance = db.Column(db.Float, default=0.0)  # Balance based on total fee and fees paid

    is_active = db.Column(db.Boolean, default=True)

    # Relationship with Invoice
    invoices = db.relationship('Invoice', back_populates='student', lazy=True)

    # Method to generate a unique admission number
    @staticmethod
    def generate_admission_number():
        last_student = Student.query.order_by(Student.id.desc()).first()
        if last_student:
            last_number = int(last_student.admission_number[3:])  # Extract the number part of the admission number
            new_number = f"AJA{last_number + 1:02d}"  # Increment the admission number
        else:
            new_number = "AJA01"  # First admission number
        return new_number

    # Method to calculate total fee based on grade and optional fees
    def calculate_total_fee(self):
        # Base fee per grade
        grade_fee = 0
        if self.grade in ['Playgroup', 'PP1', 'PP2']:
            grade_fee = 6500
        elif self.grade in ['Grade1', 'Grade2', 'Grade3']:
            grade_fee = 8500
        elif self.grade in ['Grade4', 'Grade5', 'Grade6']:
            grade_fee = 9000
        elif self.grade in ['Grade7', 'Grade8', 'Grade9']:
            grade_fee = 12000

        # Adding optional fees
        total = grade_fee
        if self.food:
            total += 3500
        if self.text_books_fee:
            total += 6000
        if self.exercise_books_fee:
            total += 500
        if self.assesment_tool_fee:
            total += 300
        if self.transport_mode == 'OneWay':
            total += 4500
        elif self.transport_mode == 'TwoWayTown':
            total += 7000
        elif self.transport_mode == 'TwoWayUma':
            total += 8000

        # Set the total fee and calculate balance
        self.total_fee = total
        
        # Ensure fees_paid is a valid value (use 0 if it's None)
        fees_paid = self.fees_paid or 0  # If fees_paid is None, default it to 0
        
        self.balance = total - fees_paid  # Calculate balance based on fees paid and total fee
        return total  # Returning the total fee for later use

    def __repr__(self):
        return f"<Student {self.first_name} {self.family_name}>"
