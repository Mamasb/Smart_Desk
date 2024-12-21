from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import Student
from app.forms import StudentForm
from flask import Blueprint
import random
import string

main_bp = Blueprint('main_bp', __name__)

# Helper function to generate a random admission number
def generate_admission_number():
    # Generate a random admission number (example: 2024ABC1234)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Route for adding a new student
@main_bp.route('/secretary/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()

    if form.validate_on_submit():
        try:
            # Log form data for debugging
            print("Form Data: ", form.data)

            # Generate a unique admission number
            admission_number = generate_admission_number()

            # Create a new student from the form data
            student = Student(
                admission_number=admission_number,  # Set the generated admission number
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                family_name=form.family_name.data,
                grade=form.grade.data,
                fees_paid=form.fees_paid.data,
                is_active=True,  # Default active
                food=form.food.data,
                text_books_fee=form.text_books_fee.data,
                exercise_books_fee=form.exercise_books_fee.data,
                assesment_tool_fee=form.assesment_tool_fee.data,
                transport_mode=form.transport_mode.data,
            )

            # Calculate and set the total fee
            total_fee = student.calculate_total_fee()
            student.total_fee = total_fee

            # Add and commit student to the database
            db.session.add(student)
            db.session.commit()

            # Check if the student was added successfully
            if student.id:
                flash(f"Student '{student.first_name} {student.family_name}' successfully added!", "success")
            else:
                flash("An error occurred while adding the student. Please try again.", "danger")
            
            return redirect(url_for('main_bp.manage_students'))

        except Exception as e:
            db.session.rollback()  # Ensure rollback on error
            print(f"Error adding student: {e}")  # Debugging
            flash("An error occurred while adding the student. Please try again.", "danger")

    else:
        # Log validation errors for debugging
        if form.errors:
            print("Validation errors: ", form.errors)
            flash("Please correct the errors in the form and try again.", "danger")

    # Render the form again if not submitted or validation failed
    return render_template('secretary/add_student.html', form=form)

# Route for editing an existing student
@main_bp.route('/secretary/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)  # Pre-populate the form with existing student data

    if form.validate_on_submit():
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

        # Recalculate the total fee based on the updated data
        total_fee = student.calculate_total_fee()
        student.total_fee = total_fee  # Update the total fee field

        try:
            db.session.commit()
            flash("Student details updated successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash("An error occurred while updating the student details. Please try again.", "danger")
        
        return redirect(url_for('main_bp.manage_students'))
    
    return render_template('secretary/edit_student.html', student=student, form=form)

# Route for generating an invoice for a student
@main_bp.route('/secretary/generate_invoice/<int:student_id>', methods=['GET'])
def generate_invoice(student_id):
    student = Student.query.get_or_404(student_id)
    total_fee = student.calculate_total_fee()

    # You can later add logic for generating a PDF instead of rendering HTML
    return render_template('secretary/invoice.html', student=student, total_fee=total_fee)

# Manage students route (list of students, manage actions)
@main_bp.route('/secretary/manage_students', methods=['GET'])
def manage_students():
    # Implement search and grade filtering
    search_query = request.args.get('search_query', '')
    grade_filter = request.args.get('grade', '')

    # Query students based on search query and grade filter
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

    grades = ["Playgroup", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9"]
    return render_template('secretary/manage_students.html', students=students, grades=grades, grade_filter=grade_filter)

# Route for deleting a student
@main_bp.route('/secretary/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student successfully deleted!", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash("An error occurred while deleting the student. Please try again.", "danger")
    
    return redirect(url_for('main_bp.manage_students'))
