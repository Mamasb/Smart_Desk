from . import db
from datetime import datetime, timedelta

# Invoice model to represent the invoice for a student
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid_date = db.Column(db.Date, nullable=True)

    # Relationship with Student
    student = db.relationship('Student', back_populates='invoices')

    def __repr__(self):
        return f"<Invoice {self.id} for {self.student.first_name} {self.student.family_name}>"

# Student model to represent a student record
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(10), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    family_name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(20), nullable=False)

    # Optional fees and options
    food = db.Column(db.Boolean, default=False)
    text_books_fee = db.Column(db.Boolean, default=False)  # True if textbooks are needed
    exercise_books_fee = db.Column(db.String(10), nullable=True)  # 'termly' or 'yearly'
    assesment_tool_fee = db.Column(db.Boolean, default=False)  # True if required
    activity_fee = db.Column(db.Boolean, default=False)  # Activity fee added
    transport_mode = db.Column(db.String(20), nullable=True)  # 'OneWay', 'TwoWayTown', 'TwoWayUma'
    
    # Financial fields
    transport_fee = db.Column(db.Float, default=0.0)  # Dynamic based on transport_mode
    total_fee = db.Column(db.Float, default=0.0)
    fees_paid = db.Column(db.Float, default=0.0)  # Ensuring a default value for fees_paid
    balance = db.Column(db.Float, default=0.0)

    is_active = db.Column(db.Boolean, default=True)

    # Relationship with Invoice
    invoices = db.relationship('Invoice', back_populates='student', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def generate_admission_number():
        """Generate a unique admission number."""
        last_student = Student.query.order_by(Student.id.desc()).first()
        if last_student:
            try:
                last_number = ''.join(filter(str.isdigit, last_student.admission_number))
                if last_number.isdigit():
                    new_number = f"AJA{int(last_number) + 1:02d}"
                else:
                    new_number = "AJA01"
            except Exception:
                new_number = "AJA01"
        else:
            new_number = "AJA01"
        return new_number

    def calculate_total_fee(self):
        """Calculate the total fee for the student based on their grade and selected options."""
        
        # Tuition Fees by Grade
        tuition_fees = {
            "Playgroup": 6500,
            "PP1": 6500,
            "PP2": 6500,
            "Grade1": 8500,
            "Grade2": 8500,
            "Grade3": 8500,
            "Grade4": 9000,
            "Grade5": 9000,
            "Grade6": 9000,
            "Grade7": 12000,
            "Grade8": 12000,
            "Grade9": 12000,
        }

        # Optional Fees
        food_fee = 3500  # Food fee
        text_books_fee = 6000  # Textbooks fee
        exercise_books_fee_termly = 500  # Exercise books termly fee
        exercise_books_fee_yearly = 1500  # Exercise books yearly fee
        assessment_tool_fee = 300  # Assessment tools fee
        activity_fee = 1000  # New activity fee

        # Transport Fees Mapping
        transport_fees = {
            "OneWay": 4500,
            "TwoWayTown": 7000,
            "TwoWayUma": 8000,
        }

        # Start with tuition fee (based on grade)
        tuition_fee = tuition_fees.get(self.grade, 0)
        print(f"Grade: {self.grade}, Tuition Fee: {tuition_fee}")  # Debugging line to print the tuition fee

        total = tuition_fee  # Initialize total with tuition fee

        # Add optional fees
        if self.food:
            total += food_fee
        if self.text_books_fee:
            total += text_books_fee
        if self.exercise_books_fee == "yearly":
            total += exercise_books_fee_yearly
        else:
            total += exercise_books_fee_termly
        if self.assesment_tool_fee:
            total += assessment_tool_fee
        if self.activity_fee:  # Add activity fee if selected
            total += activity_fee
        if self.transport_mode in transport_fees:
            total += transport_fees[self.transport_mode]

        # Update the balance (difference between total and fees already paid)
        self.total_fee = total
        self.balance = total - (self.fees_paid or 0)
        return total

    def create_invoice(self):
        """Create an invoice for the student."""
        total_fee = self.calculate_total_fee()
        due_date = datetime.now() + timedelta(days=30)

        invoice = Invoice(
            student_id=self.id,
            amount_due=total_fee,
            due_date=due_date.date(),
            paid_date=None
        )

        db.session.add(invoice)
        db.session.commit()
        return invoice

    def __repr__(self):
        middle_name = self.middle_name if self.middle_name else ""
        return f"<Student {self.first_name} {middle_name} {self.family_name}>"
