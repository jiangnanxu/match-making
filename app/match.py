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

@app.route('/match', methods=['GET', 'POST'])
def match():
	Results.query.delete()
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
			if(per.perfage=="all"):
				score = score + 2
			if(per.perfage=="El"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.perfage=="Be"):
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
			if(per.perfstate=="same"):
				if(users.state==out.state):
					score = score + 2
			if(per.percity=="all"):
				score = score + 2
			if(per.perfeducation=="any"):
				score = score + 2
			if(per.perfeducation=="Tertiary Degree"):
				if(users.education==out.education) or (users.income=="Tertiary Degree"):
					score = score + 2
			if(per.perfeducation=="Master/Phd"):
				if(users.education==out.education):
					score = score + 2
			tscore = 0
			if(tper.perfage=="all"):
				tscore = tscore + 2
			if(tper.perfage=="El"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.perfage=="Be"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.prefstate=="same"):
				if(users.state==out.state):
					tscore = tscore + 2
			if(tper.perfstate=="all"):
				tscore = tscore + 2
			if(tper.prefpersonality=="introverted"):
				if(out.personality=="introverted"):
					tscore = score + 2
				if(out.personality=="neutral"):
					tscore = score + 1
			if(tper.prefpersonality=="extroverted"):
				if(out.personality=="extroverted"):
					tscore = score + 2
				if(out.personality=="neutral"):
					tscore = score + 1
			if(tper.prefpersonality=="neutral"):
				if(users.personality=="neutral"):
					tscore = score + 2
				else:
					tscore = score + 1
			if(tper.perfeduction=="any"):
				tscore = tscore + 2
			if(tper.perfeducation=="Tertiary Degree"):
				if(users.education==out.education) or (out.education=="Master/Phd"):
					tscore = tscore + 2
			if(tper.perfeducation=="Master/Phd"):
				if(users.education==out.education):
					tscore = tscore + 2
			sm = float(tscore/8) + float(score/8)
			fsm = "{:.0%}".format(sm/2)
			result = Result(user.id, users.name, str(fsm))
			db.session.add(result)
			db.session.commit()
		else:
			return "Object not found"
	return redirect(url_for('result'))
	
			

if __name__ == "__main__":
	app.run()