from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import Student
from app.forms import StudentForm
from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

# Route for adding a new student
@main_bp.route('/secretary/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()

    if form.validate_on_submit():
        # Create a new student from the form data
        student = Student(
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            family_name=form.family_name.data,
            grade=form.grade.data,
            fees_paid=form.fees_paid.data,  # Ensure this attribute is available in your form
            is_active=True,  # Assuming the student is active by default
            food=form.food.data,
            text_books_fee=form.text_books_fee.data,
            exercise_books_fee=form.exercise_books_fee.data,
            assesment_tool_fee=form.assesment_tool_fee.data,
            transport_mode=form.transport_mode.data,
        )

        # Calculate the total fee
        total_fee = student.calculate_total_fee()

        # Update the total fee and save to the database
        student.total_fee = total_fee

        try:
            db.session.add(student)
            db.session.commit()
            flash("Student successfully added!", "success")
            return redirect(url_for('main_bp.manage_students'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash("An error occurred while adding the student. Please try again.", "danger")
            return render_template('secretary/add_student.html', form=form)

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
    students = Student.query.all()
    return render_template('secretary/manage_students.html', students=students)

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
