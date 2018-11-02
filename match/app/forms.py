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

    state = SelectField('state',choices=[('Vic','victoria'),('Nsw','new south wales'),('Wa','western Australia'),('QSL','queensland'),('Sa','south australia'),('Tas','Tasmina')])
    
    age = IntegerField('Age', validators=[DataRequired(), number_range(min=18, max=99)])
     
    gender = SelectField('gender', choices=[('M','Male'),('F','Female')])
   
    education = SelectField('Education', choices=[('highschool','highschool'),('tertiary','tertiary degree'),('master','master/phd')])

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
    
    state = SelectField('State', choices=[('Vic','victoria'),('Nsw','new south wales'),('Wa','western Australia'),('QSL','queensland'),('Sa','south australia'),('Tas','Tasmina')])
    
    personality = SelectField('Personality', choices=[('neutral','neutral'),('extroverted','extroverted'),('introverted','introverted')])
   
    education = SelectField('Education', choices=[('highschool','highschool'),('tertiary','tertiary degree'),('master','master/phd')])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


class PreferencesForm(FlaskForm):
    prefstate = SelectField('state preference', choices=[('same state','same state'), ('any', 'any state')])
    
    prefage = SelectField('Age preference', choices=[('older','older'),('younger','younger'),('any','any')] )
    
    prefpersonality = SelectField('Personality preference', choices=[('neutral','neutral'),('extroverted','extroverted'),('introverted','introverted')])
   
    prefeducation = SelectField('Education preference', choices=[('any','any'),('tertiary degree','tertiary degree'),('master/phd','master/phd')])
    
    submit = SubmitField('Update Preferences')
    
