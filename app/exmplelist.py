# -*- coding: utf-8 -*-
import sqlite3
import random

conn = sqlite3.connect('site.db')

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY, username TEXT, email TEXT, image_file TEXT, password TEXT, state TEXT, age INTEGER, gender TEXT, education TEXT, personality TEXT, posts TEXT, preferences TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Preferences(preferencesid INTERGER PRIMARY KEY, prefage INTERGER, prefstate TEXT, prefpersonality TEXT, prefeducation TEXT, username TEXT, FOREIGN KEY(username) REFERENCES User(id) )")
c.execute("CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, uid INTEGER, name TEXT, score TEXT)")

rchars="abcdedfhijklmnopqrstuvwxyz1234567890"
stlist=['VIC','NSW','QSL','SA','TAS','WA']
fm=['F','M']
edlist=['highschool','tertiary','master']
stc=['same state','any']
agepr=['older','younger','any']
edpre=['any','tertiary','master/phd']
pepre=['neutral','extroverted','introverted']



	
	
def inputdata():
	
	username=value = "".join(random.choice(rchars) for _ in range(5)) 
	email=username +"@gmail.com"
	password="123"
	state=random.choice(stlist)
	age=random.randrange(18,55)
	gender=random.choice(fm)
	education=random.choice(edlist)
	image_file="default"
			
	c.execute("INSERT INTO User(username, email, image_file, password, state, age, gender, education) VALUES(?,?,?,?,?,?,?,?)",
	(username,email, image_file, password, state, age, gender, education))
	conn.commit()
	
def inpre():
	prefage=random.choice(agepr)
	prefstate=random.choice(stc)
	prefpersonality=random.choice(pepre)
	prefeducation=random.choice(edpre)
	username="".join(random.choice(rchars) for _ in range(5)) 
		
	c.execute("INSERT INTO Preferences(prefage, prefstate, prefeducation, prefpersonality, username) VALUES(?,?,?,?,?)",
	(prefage,prefstate,prefeducation,prefpersonality,username))
	conn.commit()

for i in range(100):
	inputdata()
	inpre()
c.close()
conn.close()
