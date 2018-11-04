from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError,number_range
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=10)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(),length(min=3, max=10)])
  
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])

    state = SelectField('state',choices=[('Victoria','Victoria'),('New South Wales','New South Wales'),('Western Astralia','Western Australia'),('Queensland','Queensland'),('South Australia','South Australia'),('Tasmina','Tasmina'),('Astralia Capital Territory','Australia Capital Territory')])
    
    age = IntegerField('Age', validators=[DataRequired(), number_range(min=18, max=99)])
     
    gender = SelectField('gender', choices=[('Male','Male'),('Female','Female')])
   
    education = SelectField('Education', choices=[('Highschool','Highschool'),('Tertiary degree','Tertiary degree'),('Master/phd','Master/phd')])

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
    email = StringField('Email', validators=[DataRequired(), Email()])
	
    password = PasswordField('Password', validators=[DataRequired()])
  
    remember = BooleanField('remember me')
    submit = SubmitField('Login')

class deleteUserForm(FlaskForm):
      username = StringField('enter username for delete')
      submit = SubmitField('Delete')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    age = IntegerField('Age', validators=[DataRequired(), number_range(min=18, max=99)])
    
    state = SelectField('state',choices=[('Victoria','Victoria'),('New South Wales','New South Wales'),('Western Astralia','Western Australia'),('Queensland','Queensland'),('South Australia','South Australia'),('Tasmina','Tasmina'),('Astralia Capital Territory','Australia Capital Territory')])
    
    personality = SelectField('Personality', choices=[('Neutral','Neutral'),('Extroverted','Extroverted'),('Introverted','Introverted')])
   
    education = SelectField('Education', choices=[('Highschool','Highschool'),('Tertiary degree','Tertiary degree'),('Master/phd','Master/phd')])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


class PreferencesForm(FlaskForm):
    prefstate = SelectField('state preference', choices=[('Same state','Same state'), ('Any state', 'Any state')])
    
    prefage = SelectField('Age preference', choices=[('Older','Older'),('Younger','Younger'),('Any','Any')] )
    
    prefpersonality = SelectField('Personality preference', choices=[('Neutral','Neutral'),('Extroverted','Extroverted'),('Introverted','Introverted')])
   
    prefeducation = SelectField('Education preference', choices=[('Any','Any'),('Tertiary degree','Tertiary degree'),('Master/phd','Master/phd')])
    
    submit = SubmitField('Update Preferences')
    
