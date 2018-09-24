import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, deleteUserForm, PreferencesForm
from app.models import User, Post, Preferences
from flask_login import login_user, current_user, logout_user, login_required


posts1 = [
    {
        'author': 'master yi',
        'title': 'match making 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'akali',
        'title': 'match making 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    
    
    return render_template('home.html',title='home')
   
@app.route("/display")
def display():
    prefs=Preferences.query.all()

    return render_template('display.html',title='display', prefs=prefs)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/profile")
def profile():
    return render_template('profile.html',title='profile')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, state=form.state.data, age=form.age.data, gender=form.gender.data, education=form.education.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        

        if user and bcrypt.check_password_hash(user.password, form.password.data):
              login_user(user, remember=form.remember.data)
              next_page = request.args.get('next')
        elif  user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/admin",methods=['GET', 'POST'])
@login_required
def admin():
    posts = User.query.all()
    form=deleteUserForm()
    if form.validate_on_submit():
       user=User.query.filter_by(username=form.username.data).first()
    
       db.session.delete(user)
       db.session.commit()
       flash('selected user has been deleted!', 'success')
       next_page = request.args.get('next')
       return redirect(next_page) if next_page else redirect(url_for('admin'))
    return render_template('admin.html', title='Admin',posts=posts,form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.state = form.state.data
        current_user.personality = form.personality.data
        current_user.education = form.education.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.state.data = current_user.state
        form.personality.data = current_user.personality
        form.education.data = current_user.education
        
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/preferences", methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()
    if form.validate_on_submit():
        
        preferences = Preferences(prefage=form.prefage.data, prefstate=form.prefstate.data, prefpersonality=form.prefpersonality.data,        prefeducation=form.prefeducation.data, username=current_user.username)
        
        db.session.add(preferences)
        db.session.commit()
        
        flash('Your preference has been created! You are now able to match', 'success')
        return redirect(url_for('login'))
    return render_template('preferences.html', title='preferences', form=form)
    