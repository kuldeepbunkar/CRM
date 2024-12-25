from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange

class PropertyForm(FlaskForm):
    name = StringField('Property Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    price = FloatField('Price', validators=[NumberRange(min=0)])
    property_type = SelectField('Type', choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial')
    ])

class LeadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    source = StringField('Source') 