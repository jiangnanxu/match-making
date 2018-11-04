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
    
    return render_template('home.html',title='home')
   
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

@app.route("/record")
def record():
    return render_template('record.html',title='our legal record statement')

@app.route("/privacy")
def privacy():
    return render_template('privacy.html',title='privacy statement')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('display'))
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
		return redirect(url_for('display'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if form.email.data=='admin@gmail.com' and form.password.data=='admin':
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
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.age = form.age.data
		current_user.state = form.state.data
		current_user.personality = form.personality.data
		current_user.education = form.education.data
		current_user.height = form.height.data
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		db.session.commit()
		flash('Your setting has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.age.data = current_user.age
		form.state.data = current_user.state
		form.personality.data = current_user.personality
		form.education.data = current_user.education
		form.height.data = current_user.height
	
	return render_template('account.html', title='account', image_file=image_file, form=form)

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

@app.route("/preferences", methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()
    if form.validate_on_submit():
		
        preferences = Preferences(prefage=form.prefage.data, prefstate=form.prefstate.data, prefpersonality=form.prefpersonality.data, prefeducation=form.prefeducation.data, perfheight=form.perfheight.data, username=current_user.username)
        Preferences.query.filter_by(username=current_user.username).delete()
        db.session.add(preferences)
        db.session.commit()
        
        flash('Your preference has been created! You are now able to match', 'success')
        next_page = request.args.get('next')
        return  redirect(next_page) if next_page else redirect(url_for('display'))
    return render_template('preferences.html', title='preferences', form=form)

@app.route("/run", methods=['GET', 'POST'])
def run():
	fo = Preferences.query.filter_by(username=current_user.username)
	per = fo.first()
	if per:
		return redirect(url_for('match'))
	else:
		flash('You need to create your preferences before you match!')
		return redirect(url_for('display'))
	
	
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
			if(per.prefage=="Any"):
				score = score + 2
			if(per.prefage=="Younger"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.prefage=="Older"):
				if(users.age==out.age)or(out.age < users.age):
					score = score + 2
			if(per.prefpersonality=="Introverted"):
				if(users.personality=="Introverted"):
					score = score + 2
				if(users.personality=="Neutral"):
					score = score + 1
			if(per.prefpersonality=="Extroverted"):
				if(users.personality=="Extroverted"):
					score = score + 2
				if(users.personality=="Neutral"):
					score = score + 1
			if(per.prefpersonality=="Neutral"):
				if(users.personality=="Neutral"):
					score = score + 2
				else:
					score = score + 1
			if(per.prefstate=="Any"):
				score = score + 2
			if(per.prefstate=="Same state"):
				if(users.state==out.state):
					score = score + 2
			if(per.prefeducation=="Any"):
				score = score + 2
			if(per.prefeducation=="Tertiary degree"):
				if(users.education==out.education) or (users.education=="Tertiary degree"):
					score = score + 2
			if(per.prefeducation=="Master/Phd"):
				if(users.education==out.education):
					score = score + 2
			if(per.perfheight=="Any"):
				score = score + 2
			if(per.perfheight=="Higher"):
				if(users.height==out.height) or (users.height < out.height):
					score = score + 2
			if(per.perfheight=="Lower"):
				if(users.height==out.height) or (users.height > out.height):
					score = score + 2	
			tscore = 0
			if(tper.prefage=="Any"):
				tscore = tscore + 2
			if(tper.prefage=="Younger"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.prefage=="Older"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.prefstate=="Same state"):
				if(users.state==out.state):
					tscore = tscore + 2
			if(tper.prefstate=="Any"):
				tscore = tscore + 2
			if(tper.prefpersonality=="Introverted"):
				if(out.personality=="Introverted"):
					tscore = tscore + 2
				if(out.personality=="Neutral"):
					tscore = tscore + 1
			if(tper.prefpersonality=="Extroverted"):
				if(out.personality=="Extroverted"):
					tscore = tscore + 2
				if(out.personality=="Neutral"):
					tscore = tscore + 1
			if(tper.prefpersonality=="Neutral"):
				if(users.personality=="Neutral"):
					tscore = tscore + 2
				else:
					tscore = tscore + 1
			if(tper.prefeducation=="Any"):
				tscore = tscore + 2
			if(tper.prefeducation=="Tertiary degree"):
				if(users.education==out.education) or (out.education=="Master/Phd"):
					tscore = tscore + 2
			if(tper.prefeducation=="Master/Phd"):
				if(users.education==out.education):
					tscore = tscore + 2
			if(tper.perfheight=="Any"):
				tscore = tscore + 2
			if(tper.perfheight=="Higher"):
				if(users.height==out.height) or (users.height > out.height):
					tscore = tscore + 2
			if(tper.perfheight=="Lower"):
				if(users.height==out.height) or (users.height < out.height):
					tscore = tscore + 2
			sm = float(tscore/10) + float(score/10)
			fsm = "{:.0%}".format(sm/2)
			result = results(uid=users.id, name=users.username, score=str(fsm), state=users.state, education=users.education, image_file=users.image_file, age=users.age, personality=users.personality, height=users.height)
			db.session.add(result)
			db.session.commit()
	page=request.args.get('page',1,type=int)
	return render_template('result.html',title='match', results=results.query.order_by(results.score.desc()).paginate(page=page, per_page=5))
	
	
	     
