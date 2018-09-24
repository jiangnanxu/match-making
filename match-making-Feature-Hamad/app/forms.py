from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField, SelectMultipleField, widgets
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError,number_range
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=10)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(),length(min=3, max=10)])
  
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])

    state = SelectField('State', choices=[('vic','VIC'), ('nsw', 'NSW'),('qsl','QSL'), ('sa', 'SA'), ('tas', 'TAS')])
    
    age = IntegerField('Age', validators=[DataRequired(), number_range(min=18, max=99)])
     
    gender = SelectField('Gender', choices=[('M','Male'),('F','Female')])
   
    education = SelectField('Education', choices=[('HS','Highschool'),('TD','Tertiary'),('UN','Undergrade'),('MD','Masters'),('PhD','PhD')])

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

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    age = IntegerField('Age', validators=[DataRequired(), number_range(min=18, max=99)])
    
    state = SelectField('State', choices=[('vic','VIC'), ('nsw', 'NSW'),('qsl','QSL'), ('sa', 'SA'), ('tas', 'TAS')])
    
    personality = SelectField('Personality', choices=[('E','Extroverted'), ('I','Introverted') , ('N','No preference')])
   
    education = SelectField('Education', choices=[('HS','Highschool'),('TD','Tertiary'),('UN','Undergrade'),('MD','Masters'),('PhD','PhD')])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
                

class deleteUserForm(FlaskForm):
      username = StringField('enter username for delete')
      submit = SubmitField('Delete')



class PreferencesForm(FlaskForm):
    
    prefage = SelectField('Age preference', choices=[('old','Older'),('young','Younger'), ('same age','Same age'), ('No pref','No preference')] )
    
    prefstate = SelectField('State preference', choices=[('Local','Local'), ('No pref', 'No preference')])
    
    prefpersonality = SelectField('Personality preference', choices=[('E','Extroverted'), ('I','Introverted') , ('N','No preference')])
   
    prefeducation = SelectField('Education preference', choices=[('HS','Highschool'),('TD','Tertiary'),('UN','Undergrade'),('MD','Masters'),('PhD','PhD')])
    
    submit = SubmitField('Update Preferences')