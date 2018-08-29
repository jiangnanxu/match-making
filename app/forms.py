from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
  
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
         user=User.query.filter_by(username=username.data).first()
         if user:
            raise ValidationError('that username is taken. please try again')
    
    def validate_email(self, email):
         user=User.query.filter_by(email=email.data).first()
         if user:
            raise ValidationError('that email is taken. please try again')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    
    password = PasswordField('Password', validators=[DataRequired()])
  
    remember = BooleanField('remember me')
    submit = SubmitField('Login')
    