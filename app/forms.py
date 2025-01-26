from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, FloatField
from wtforms.validators import DataRequired

# Student form
class StudentForm(FlaskForm):
    # Personal Information Fields
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    family_name = StringField('Family Name')

    # Grade Selection
    grade = SelectField('Grade', choices=[
        ('Playgroup', 'Playgroup'), 
        ('PP1', 'PP1'), 
        ('PP2', 'PP2'), 
        ('Grade1', 'Grade1'), 
        ('Grade2', 'Grade2'), 
        ('Grade3', 'Grade3'), 
        ('Grade4', 'Grade4'), 
        ('Grade5', 'Grade5'), 
        ('Grade6', 'Grade6'), 
        ('Grade7', 'Grade7'), 
        ('Grade8', 'Grade8'), 
        ('Grade9', 'Grade9')
    ], validators=[DataRequired()])

    # Fee-related Fields
    food = BooleanField('Food')
    text_books_fee = BooleanField('Text Books')
    exercise_books_fee = BooleanField('Exercise Books')
    assesment_tool_fee = BooleanField('Assessment Tools')

    # Transport-related Fields
    transport_mode = SelectField('Transport Mode', choices=[
        ('None', 'None'), 
        ('OneWay', 'One-Way'), 
        ('TwoWayTown', 'Two-Way (Town)'), 
        ('TwoWayUma', 'Two-Way (Uma)')
    ], default='None')

    # Optional transport fee (editable)
    transport_fee = FloatField('Transport Fee', default=0.0)

    # Payment Fields
    fees_paid = FloatField('Fees Paid', default=0.0)

    # Balance Field (added this field)
    balance = FloatField('Balance', default=0.0)  # Add balance field here

    # Total Fee (Calculated)
    total_fee = FloatField('Total Fee', default=0.0, render_kw={'readonly': True})

# Payment form
class PaymentForm(FlaskForm):
    # Payment Method Field
    payment_method = SelectField('Payment Method', choices=[
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Mobile Payment', 'Mobile Payment'),
        ('Credit Card', 'Credit Card')
    ], validators=[DataRequired()])

    # Payment Amount Field
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])

    # Payment Date Field
    payment_date = StringField('Payment Date', validators=[DataRequired()])

    # Remaining Balance
    remaining_balance = FloatField('Remaining Balance', default=0.0, render_kw={'readonly': True})
