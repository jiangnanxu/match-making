from __future__ import division
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from table import *
engine = create_engine('sqlite:///site.db', echo=True)

app = Flask(__name__)

@app.route('/display')
def display():
	return render_template('show.html', results = results.query.all())

@app.route('/')
def main():
	return render_template('new.html')

@app.route('/input', methods=['GET', 'POST'])
def importuser():
	Result.query.delete()
	fs = User.query.filter_by(current_user.username)
	out = fs.first()
	fo = Preferences.query.filter_by(current_user.username)
	per = fo.first()
	result = User.query.filter_by(User.gender != out.gender).all()
	for users in result:
		tout = Preferences.query.filter_by(Preferences.name == users.name)
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
				else
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
				if(users.education==out.education)
					score = score + 2
			tscore = 0
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
				else
					score = score + 1
			if(tper.perfeduction=="High School Graduate"):
				tscore = tscore + 2
			if(tper.perfeducation=="Tertiary Degree"):
				if(users.education==out.education) or (out.education=="Master/Phd"):
					tscore = tscore + 2
			if(tper.perfeducation=="Master/Phd"):
				if(users.education==out.education)
					tscore = tscore + 2
			sm = float(tscore/6) + float(score/6)
			fsm = "{:.0%}".format(sm/2)
			result = Result(users.name, str(fsm), users.id)
			db.session.add(result)
			db.session.commit()
		else:
			return "Object not found"
	return redirect(url_for('display'))
	
	
			

if __name__ == "__main__":
	app.run()