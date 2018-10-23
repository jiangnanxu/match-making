from __future__ import division
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from table import *
engine = create_engine('sqlite:///data.db', echo=True)

app = Flask(__name__)


@app.route('/')
def main():
	return render_template('new.html')

@app.route('/input', methods=['GET', 'POST'])
def importuser():
	
	POST_NAME = request.form['username']
	
	Session = sessionmaker(bind=engine)
	s = Session()
	fs = s.query(User).filter(User.name.in_([POST_NAME]))
	out = fs.first()
	fo = s.query(Per).filter(Per.name.in_([POST_NAME]))
	per = fo.first()
	ts = s.query(User).filter(User.gender != out.gender)
	tout = ts.first()
	to = s.query(Per).filter(Per.name == tout.name)
	tper = to.first()
	if tout:
		score = 0
		if(per.perage=="All"):
			score = score + 2
		if(per.perage=="EL"):
			if(tout.age==out.age)or(out.age > tout.age):
				score = score + 2
		if(per.perage=="BE"):
			if(tout.age==out.age)or(out.age < tout.age):
				score = score + 2
		if(per.peradd=="Same"):
			if(tout.address==out.address):
				score = score + 2
		if(per.peradd=="All"):
			score = score + 2
		if(per.perin=="All"):
			score = score + 2
		if(per.perin=="LE"):
			if(tout.income==out.income) or (out.income > tout.income):
				score = score + 2
		if(per.perin=="HE"):
			if(tout.income==out.income) or (out.income < tout.income):
				score = score + 2
			
	if tper:
		tscore = 0
		if(tper.perage=="All"):
			tscore = tscore + 2
		if(tper.perage=="EL"):
			if(tout.age==out.age)or(tout.age > out.age):
				tscore = tscore + 2
		if(tper.perage=="BE"):
			if(tout.age==out.age)or(tout.age < out.age):
				tscore = tscore + 2
		if(tper.peradd=="Same"):
			if(tout.address==out.address):
				tscore = tscore + 2
		if(tper.peradd=="All"):
			tscore = tscore + 2
		if(tper.perin=="All"):
			tscore = tscore + 2
		if(tper.perin=="LE"):
			if(tout.income==out.inceme) or (tout.income > out.income):
				tscore = tscore + 2
		if(per.perin=="HE"):
			if(tout.income==out.income) or (tout.income < out.income):
				tscore = tscore + 2
	else:
		return "Object not found"
	sm = float(tscore/6) + float(score/6)
	fsm = "{:.0%}".format(sm/2)
	return "Name: " + tout.name + " " + "Result: " + str(fsm)
			

if __name__ == "__main__":
	app.run()