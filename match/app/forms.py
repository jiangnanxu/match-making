from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
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
     
    gender = SelectField('gender',choices=[('M','Male'),('F','Female')])
   
    education = SelectField('Education',choices=[('hs','highschool'),('td','tertiary degree'),('mp','master/phd')])

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
    prefstate = SelectField('state preference', choices=[('same','same state'), ('all', 'any state')])
    
    prefage = SelectField('Age preference', choices=[('Be','older'),('El','younger'),('all','any')] )
    
    prefpersonality = SelectField('Personality preference', choices=[('ne','neutral'),('ex','extroverted'),('in','introverted')])
   
    prefeducation = SelectField('Education preference', choices=[('hs','highschool'),('td','tertiary degree'),('mp','master/phd')])
    
    submit = SubmitField('Update Preferences')
    