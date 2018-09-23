import os
import secrets

from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, deleteUserForm, PreferencesForm
from app.models import User, Post, Preferences, results
from sqlalchemy.orm import sessionmaker
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
    
    
    return render_template('homepage.html',title='home')
   
@app.route("/display")
def display():
    prefs=Preferences.query.all()

    return render_template('display.html',title='display', prefs=prefs)
@app.route('/display2')
def display2():
       res = results.query.all()
       return render_template('result.html', title='result', res=res)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/profile")
def profile():
    return render_template('profile.html',title='profile')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
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
        return redirect(url_for('account'))
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
    form= deleteUserForm()
    if form.validate_on_submit():
       user=User.query.filter_by(username=form.username.data).first()
       db.session.delete(user)
       db.session.commit()
       flash('selected user has been deleted!', 'success')
       next_page = request.args.get('next')
       return  redirect(url_for('admin'))
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
        
        preferences = Preferences(prefage=form.prefage.data, prefstate=form.prefstate.data, prefpersonality=form.prefpersonality.data,        prefeducation=form.prefeducation.data, username=current_user.username)
        
        db.session.add(preferences)
        db.session.commit()
        
        flash('Your preference has been created! You are now able to match', 'success')
        next_page = request.args.get('next')
        return  redirect(next_page) if next_page else redirect(url_for('display'))
    return render_template('preferences.html', title='preferences', form=form)

@app.route("/test",methods=['GET','POST'])
def test():
   
   result1=results(uid=1,name='ammy',score='80%')
   db.session.add(result1)
   db.session.commit()
   
   flash('match result added to database')
   return render_template('homepage.html',title='home')

@app.route("/match", methods=['GET', 'POST'])
def match():
	results.query.delete()
	fs = User.query.filter_by(username=current_user.username)
	out = fs.first()
	fo = Preferences.query.filter_by(username=current_user.username)
	per = fo.first()
	result = User.query.filter(User.gender != out.gender).all()
	for users in result:
		tout = Preferences.query.filter(Preferences.username == users.username)
		tper = tout.first()
		if tper:
			score = 0
			if(per.prefage=="all"):
				score = score + 2
			if(per.prefage=="El"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.prefage=="Be"):
				if(users.age==out.age)or(out.age < users.age):
					score = score + 2
			if(per.prefpersonality=="in"):
				if(users.personality=="introverted"):
					score = score + 2
				if(users.personality=="ne"):
					score = score + 1
			if(per.prefpersonality=="ex"):
				if(users.personality=="extroverted"):
					score = score + 2
				if(users.personality=="ne"):
					score = score + 1
			if(per.prefpersonality=="ne"):
				if(users.personality=="neutral"):
					score = score + 2
				else:
					score = score + 1
			if(per.prefstate=="same"):
				if(users.state==out.state):
					score = score + 2
			
			if(per.prefeducation=="any"):
				score = score + 2
			if(per.prefeducation=="Tertiary Degree"):
				if(users.education==out.education) or (users.income=="Tertiary Degree"):
					score = score + 2
			if(per.prefeducation=="Master/Phd"):
				if(users.education==out.education):
					score = score + 2
			tscore = 0
			if(tper.prefage=="all"):
				tscore = tscore + 2
			if(tper.prefage=="El"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.prefage=="Be"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.prefstate=="same"):
				if(users.state==out.state):
					tscore = tscore + 2
			if(tper.prefstate=="all"):
				tscore = tscore + 2
			if(tper.prefpersonality=="introverted"):
				if(out.personality=="introverted"):
					tscore = tscore + 2
				if(out.personality=="neutral"):
					tscore = tscore + 1
			if(tper.prefpersonality=="extroverted"):
				if(out.personality=="extroverted"):
					tscore = tscore + 2
				if(out.personality=="neutral"):
					tscore = tscore + 1
			if(tper.prefpersonality=="neutral"):
				if(users.personality=="neutral"):
					tscore = tscore + 2
				else:
					tscore = tscore + 1
			if(tper.prefeducation=="any"):
				tscore = tscore + 2
			if(tper.prefeducation=="Tertiary Degree"):
				if(users.education==out.education) or (out.education=="Master/Phd"):
					tscore = tscore + 2
			if(tper.prefeducation=="Master/Phd"):
				if(users.education==out.education):
					tscore = tscore + 2
			sm = float(tscore/8) + float(score/8)
			fsm = "{:.0%}".format(sm/2)
			result = results(uid=users.id, name=users.username, score=str(fsm))
			db.session.add(result)
			db.session.commit()
		else:
			return "Object not found"
	return render_template('match.html',title='match', result=result)
	
	
	     