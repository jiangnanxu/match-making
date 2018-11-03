import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, deleteUserForm, PreferencesForm
from app.models import User, Post, Preferences, results
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    
    return render_template('homepage.html',title='home')
   
@app.route("/display")
def display():
	image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
	prefs=Preferences.query.filter_by(username=current_user.username)
	users=User.query.filter_by(username=current_user.username)
	return render_template('display.html',title='display', image_file=image_file, prefs=prefs, users=users)

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
		if form.email.data=='admin@gmail.com':
			if bcrypt.check_password_hash(admin, form.password.data):
				login_user(user, remember=form.remember.data)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('admin'))
		elif user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('display'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/admin",methods=['GET', 'POST'])

def admin():
    page=request.args.get('page',1,type=int)
    posts = User.query.paginate(page=page, per_page=10)
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
	image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
	if form.validate_on_submit():	
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
	
	return render_template('account.html', title='Account', image_file=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 

@app.route("/preferences", methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()
    if form.validate_on_submit():
		
        preferences = Preferences(prefage=form.prefage.data, prefstate=form.prefstate.data, prefpersonality=form.prefpersonality.data, prefeducation=form.prefeducation.data, username=current_user.username)
        Preferences.query.filter_by(username=current_user.username).delete()
        db.session.add(preferences)
        db.session.commit()
        
        flash('Your preference has been created! You are now able to match', 'success')
        next_page = request.args.get('next')
        return  redirect(next_page) if next_page else redirect(url_for('display'))
    return render_template('preferences.html', title='preferences', form=form)


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
			if(per.prefage=="any"):
				score = score + 2
			if(per.prefage=="younger"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.prefage=="older"):
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
			if(per.prefstate=="any"):
				score = score + 2
			if(per.prefstate=="same statee"):
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
			if(tper.prefage=="any"):
				tscore = tscore + 2
			if(tper.prefage=="younger"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.prefage=="older"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.prefstate=="same state"):
				if(users.state==out.state):
					tscore = tscore + 2
			if(tper.prefstate=="any"):
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
	page=request.args.get('page',1,type=int)
			
	return render_template('result.html',title='match',results=results.query.paginate(page=page, per_page=5))

	

