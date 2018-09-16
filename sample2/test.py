from __future__ import division
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from table import *
engine = create_engine('sqlite:///data.db', echo=True)

app = Flask(__name__)

@app.route('/display')
def display():
	Session = sessionmaker(bind=engine) 
	results = Session.query(Result).all()
	return render_template('show.html', results = results)

@app.route('/')
def main():
	return render_template('new.html')

@app.route('/input', methods=['GET', 'POST'])
def importuser():
	POST_NAME = request.form['username']
	
	Session = sessionmaker(bind=engine)
	s = Session()
	s.query(Result).delete()
	fs = s.query(User).filter(User.name.in_([POST_NAME]))
	out = fs.first()
	fo = s.query(Per).filter(Per.name.in_([POST_NAME]))
	per = fo.first()
	result = s.query(User).filter(User.gender != out.gender).all()
	for users in result:
		tout = s.query(Per).filter(Per.name == users.name)
		tper = tout.first()
		if tper:
			score = 0
			if(per.perage=="All"):
				score = score + 2
			if(per.perage=="EL"):
				if(users.age==out.age)or(out.age > users.age):
					score = score + 2
			if(per.perage=="BE"):
				if(users.age==out.age)or(out.age < users.age):
					score = score + 2
			if(per.peradd=="Same"):
				if(users.address==out.address):
					score = score + 2
			if(per.peradd=="All"):
				score = score + 2
			if(per.perin=="All"):
				score = score + 2
			if(per.perin=="LE"):
				if(users.income==out.income) or (out.income > users.income):
					score = score + 2
			if(per.perin=="HE"):
				if(users.income==out.income) or (out.income < users.income):
					score = score + 2
			tscore = 0
			if(tper.perage=="All"):
				tscore = tscore + 2
			if(tper.perage=="EL"):
				if(users.age==out.age)or(users.age > out.age):
					tscore = tscore + 2
			if(tper.perage=="BE"):
				if(users.age==out.age)or(users.age < out.age):
					tscore = tscore + 2
			if(tper.peradd=="Same"):
				if(users.address==out.address):
					tscore = tscore + 2
			if(tper.peradd=="All"):
				tscore = tscore + 2
			if(tper.perin=="All"):
				tscore = tscore + 2
			if(tper.perin=="LE"):
				if(users.income==out.income) or (users.income > out.income):
					tscore = tscore + 2
			if(per.perin=="HE"):
				if(users.income==out.income) or (users.income < out.income):
					tscore = tscore + 2
			sm = float(tscore/6) + float(score/6)
			fsm = "{:.0%}".format(sm/2)
			result = Result(users.name, str(fsm), users.id)
			s.add(result)
			s.commit()
		else:
			return "Object not found"
	return render_template('show.html')
	
	
			

if __name__ == "__main__":
	app.run()