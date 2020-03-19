from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    """ Registration Form"""
    username = StringField('username')