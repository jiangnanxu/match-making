import os
import secrets

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
    
    pref=Preferences.query.all()
    return render_template('home.html',pref=pref)
   

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
        
        if user.email=='admin@gmail.com':
           if user and bcrypt.check_password_hash(user.password, form.password.data):
              login_user(user, remember=form.remember.data)
              next_page = request.args.get('next')
              return redirect(next_page) if next_page else redirect(url_for('admin'))
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

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('account.html', title='Account', form=form)

@app.route("/preferences", methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()
    if form.validate_on_submit():
        
        preferences = Preferences(prefage=form.prefage.data, prefstate=form.prefstate.data, prefpersonality=form.prefpersonality.data,        prefeducation=form.prefeducation.data, user_id=current_user.id)
        
        db.session.add(preferences)
        db.session.commit()
        
        flash('Your preference has been created! You are now able to match', 'success')
        return redirect(url_for('login'))
    return render_template('preferences.html', title='preferences', form=form)
    
 
@app.route('/match', methods=['GET', 'POST'])
def match():
	user = current_user.username
	fs=User.query.filter_by(username=user)
	out=fs.first()
	fo=Preferences.query.filter_by(user_id=out.id)
	per=fo.first()
	result=User.query.filter_by(gender != out.gender).all()
	for users in result:
		tout = Preferences.query.filter(Preferences.user_id == users.id)
		tper = tout.first()
		if tper:
			score = 0
			if(per.perfage=="All"):
				score = score + 2
			if(per.perfage=="EL"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.perfage=="BE"):
				if(users.age==out.age)or(out.age < users.age):
					score = score + 2
			if(per.prefpersonality=="introverted"):
				if(users.personality=="introverted"):
					score = score + 2
				if(users.personality=="neutral"):
					score = score + 1
			if(per.prefpersonality=="extroverted"):
				if(users.personality=="extroverted"):
					score = score + 2
				if(users.personality=="neutral"):
					score = score + 1
			if(per.prefpersonality=="neutral"):
				if(users.personality=="neutral"):
					score = score + 2
				else:
					score = score + 1
			if(per.perfcity=="Same"):
				if(users.city==out.city):
					score = score + 2
			if(per.percity=="All"):
				score = score + 2
			if(per.perfeducation=="High School Graduate"):
				score = score + 2
			if(per.perfeducation=="Tertiary Degree"):
				if(users.education==out.education) or (users.income=="Tertiary Degree"):
					score = score + 2
			if(per.perfeducation=="Master/Phd"):
				if(users.education==out.education):
					score = score + 2
			if(tper.perfage=="All"):
				tscore = tscore + 2
			if(tper.perfage=="EL"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.perfage=="BE"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.perfcity=="Same"):
				if(users.city==out.city):
					tscore = tscore + 2
			if(tper.perfcity=="All"):
				tscore = tscore + 2
			if(tper.prefpersonality=="introverted"):
				if(out.personality=="introverted"):
					score = score + 2
				if(out.personality=="neutral"):
					score = score + 1
			if(tper.prefpersonality=="extroverted"):
				if(out.personality=="extroverted"):
					score = score + 2
				if(out.personality=="neutral"):
					score = score + 1
			if(tper.prefpersonality=="neutral"):
				if(users.personality=="neutral"):
					score = score + 2
				else:
					score = score + 1
			if(tper.perfeduction=="High School Graduate"):
				tscore = tscore + 2
			if(tper.perfeducation=="Tertiary Degree"):
				if(users.education==out.education) or (out.education=="Master/Phd"):
					tscore = tscore + 2
			if(tper.perfeducation=="Master/Phd"):
				if(users.education==out.education):
					tscore = tscore + 2
			sm = float(tscore/6) + float(score/6)
			fsm = "{:.0%}".format(sm/2)
			result = Result(users.id, users.name, str(fsm))
			db.session.add(result)
			db.session.commit()
		else:
			return "Object not found"
	return redirect(url_for('display'))

@app.route('/display')
def display():
	return render_template('show.html', results = results.query.all())