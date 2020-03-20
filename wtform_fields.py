from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data
    
    user_object = User.query.filter_by(username=username_entered).first() # the value the user puts into web page
    if user_object is None: # if user_object already exists 
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password): # checks to see if the function returns false
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    """ Registration Form"""
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Pasword required"), Length(min=6, max=25, message="Password must be between 6 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Signup')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first() # the value the user puts into web page
        if user_object: # if user_object already exists 
            raise ValidationError("Username already exists. Please select a different username.")

class LoginForm(FlaskForm):
    """ Login Form """
    username = StringField('username', validators=[InputRequired(message="Username required")]) # takes in data from html form
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')