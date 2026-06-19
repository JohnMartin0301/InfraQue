from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

REQUEST_TYPES = [
    ("Virtual Machine", "Virtual Machine"),
    ("Storage Increase", "Storage Increase"),
    ("User Access", "User Access"),
    ("Application Installation", "Application Installation"),
]

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    request_type = SelectField('Request Type', choices=REQUEST_TYPES, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit Request')