from flask import render_template, redirect, url_for, flash, request, send_file
from app import db
from app.models import Student
from app.forms import StudentForm
from flask import Blueprint
import io
from reportlab.pdfgen import canvas
from datetime import datetime
from sqlalchemy.sql import or_

main_bp = Blueprint('main_bp', __name__)

# Helper function to generate a sequential admission number
def generate_admission_number():
    """Generate a unique admission number."""
    base_number = "AJA"
    last_number = 1  # Default starting point

    while True:
        admission_number = f"{base_number}{last_number:02d}"
        existing_student = Student.query.filter_by(admission_number=admission_number).first()
        if not existing_student:
            return admission_number
        last_number += 1

# Function to get a student by ID
def get_student_by_id(student_id):
    """Fetch a student record by ID or return 404 if not found."""
    return Student.query.get_or_404(student_id)

# Route for adding a new student
@main_bp.route('/secretary/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        try:
            # Check for existing student
            existing_student = Student.query.filter_by(
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                family_name=form.family_name.data,
                grade=form.grade.data
            ).first()

            if existing_student:
                flash(f"Student '{form.first_name.data} {form.family_name.data}' already exists in grade {form.grade.data}.", "warning")
                return redirect(url_for('main_bp.manage_students'))

            # Generate admission number
            admission_number = generate_admission_number()

            # Create a new student instance
            student = Student(
                admission_number=admission_number,
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                family_name=form.family_name.data,
                grade=form.grade.data,
                fees_paid=form.fees_paid.data,
                food=form.food.data,
                text_books_fee=form.text_books_fee.data,
                exercise_books_fee=form.exercise_books_fee.data,
                assesment_tool_fee=form.assesment_tool_fee.data,
                transport_mode=form.transport_mode.data,
            )
            # Calculate the total fee
            student.calculate_total_fee()

            # Save to the database
            db.session.add(student)
            db.session.commit()

            flash(f"Student '{student.first_name} {student.family_name}' successfully added!", "success")
            return redirect(url_for('main_bp.manage_students'))

        except Exception as e:
            db.session.rollback()
            print(f"Error adding student: {e}")
            flash("An error occurred while adding the student. Please try again.", "danger")

    if form.errors:
        print("Validation errors: ", form.errors)
        flash("Please correct the errors in the form and try again.", "danger")

    return render_template('secretary/add_student.html', form=form)

# Route for editing an existing student
@main_bp.route('/secretary/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = get_student_by_id(student_id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        try:
            # Update student details
            student.first_name = form.first_name.data
            student.middle_name = form.middle_name.data
            student.family_name = form.family_name.data
            student.grade = form.grade.data
            student.fees_paid = form.fees_paid.data
            student.food = form.food.data
            student.text_books_fee = form.text_books_fee.data
            student.exercise_books_fee = form.exercise_books_fee.data
            student.assesment_tool_fee = form.assesment_tool_fee.data
            student.transport_mode = form.transport_mode.data
            student.calculate_total_fee()

            db.session.commit()
            flash("Student details updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Error editing student: {e}")
            flash("An error occurred while updating the student details. Please try again.", "danger")

        return redirect(url_for('main_bp.manage_students'))

    return render_template('secretary/edit_student.html', student=student, form=form)

# Route for generating an invoice for a student
@main_bp.route('/secretary/generate_invoice/<int:student_id>', methods=['GET'])
def generate_invoice(student_id):
    student = get_student_by_id(student_id)
    total_fee = student.calculate_total_fee()  # Ensure this method is calculating the fee properly
    fees_paid = student.fees_paid or 0.0
    balance_due = total_fee - fees_paid

    return render_template(
        'secretary/invoice.html',
        student=student,
        total_fee=total_fee,
        balance=balance_due,
        current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

# Route for downloading an invoice as a PDF
@main_bp.route('/secretary/download_invoice/<int:student_id>', methods=['GET'])
def download_invoice(student_id):
    student = get_student_by_id(student_id)
    total_fee = student.calculate_total_fee()  # Ensure this method is calculating the fee properly
    fees_paid = student.fees_paid or 0.0
    balance_due = total_fee - fees_paid

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    
    # Add text to the PDF
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, f"Invoice for {student.first_name} {student.family_name}")
    pdf.drawString(100, 780, f"Admission Number: {student.admission_number}")
    pdf.drawString(100, 760, f"Grade: {student.grade}")
    pdf.drawString(100, 740, f"Total Fee: {total_fee}")
    pdf.drawString(100, 720, f"Fees Paid: {fees_paid}")
    pdf.drawString(100, 700, f"Balance Due: {balance_due}")
    pdf.drawString(100, 680, f"Food: {student.food}")
    pdf.drawString(100, 660, f"Text Books Fee: {student.text_books_fee}")
    pdf.drawString(100, 640, f"Exercise Books Fee: {student.exercise_books_fee}")
    pdf.drawString(100, 620, f"Assessment Tool Fee: {student.assesment_tool_fee}")
    pdf.drawString(100, 600, f"Transport Mode: {student.transport_mode}")
    
    # Add date and time of the invoice generation
    pdf.drawString(100, 580, f"Invoice Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{student.admission_number}.pdf", mimetype='application/pdf')

# Route for managing students
@main_bp.route('/secretary/manage_students', methods=['GET', 'POST'])
def manage_students():
    search_query = request.form.get('search_query', '').strip() if request.method == 'POST' else request.args.get('search_query', '').strip()
    grade_filter = request.form.get('grade', '').strip() if request.method == 'POST' else request.args.get('grade', '').strip()

    query = Student.query
    if search_query:
        query = query.filter(
            (Student.admission_number.like(f'%{search_query}%')) |
            (Student.first_name.like(f'%{search_query}%')) |
            (Student.middle_name.like(f'%{search_query}%')) |
            (Student.family_name.like(f'%{search_query}%'))
        )
    if grade_filter:
        query = query.filter_by(grade=grade_filter)

    students = query.all()
    grades = ["Playgroup", "PP1", "PP2", "Grade1", "Grade2", "Grade3", "Grade4", "Grade5", "Grade6", "Grade7", "Grade8", "Grade9"]

    return render_template('secretary/manage_students.html', students=students, grades=grades, grade_filter=grade_filter, search_query=search_query)

# Route for deleting a student
@main_bp.route('/secretary/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = get_student_by_id(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student successfully deleted!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting student: {e}")
        flash("An error occurred while deleting the student. Please try again.", "danger")

    return redirect(url_for('main_bp.manage_students'))
