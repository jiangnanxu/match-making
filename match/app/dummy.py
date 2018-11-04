# -*- coding: utf-8 -*-
import sqlite3
import random

conn = sqlite3.connect('site.db')

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY, username TEXT, email TEXT, image_file TEXT, password TEXT, state TEXT, age INTEGER, gender TEXT, education TEXT, personality TEXT, posts TEXT, preferences TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Preferences(preferencesid INTERGER PRIMARY KEY, prefage INTERGER, prefstate TEXT, prefpersonality TEXT, prefeducation TEXT, username TEXT, FOREIGN KEY(username) REFERENCES User(id) )")
c.execute("CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, uid INTEGER, name TEXT, score TEXT)")

rchars="abcdedfhijklmnopqrstuvwxyz1234567890"
stlist=['Victoria','New South Wales','Queensland','South Australia','Tasmina','Western Astralia','Astralia Capital Territory']
fm=['Female','Male']
edlist=['Highschool','Tertiary degree','Master/phd']
stc=['Same state','Any']
agepr=['Older','Younger','Any']
edpre=['Any','Tertiary','Master/phd']
pepre=['Neutral','Extroverted','Introverted']
pehi=['Any','Higher','Lower']




	
	
def inputdata():
	
	username=value = "".join(random.choice(rchars) for _ in range(5)) 
	email=username +"@gmail.com"
	password="123"
	state=random.choice(stlist)
	age=random.randrange(18,55)
	height=random.randrange(140,199)
	gender=random.choice(fm)
	education=random.choice(edlist)
	personality=random.choice(pepre)
	image_file="static/profile_pics/default.jpg"
			
	c.execute("INSERT INTO User(username, email, image_file, password, state, age, height, gender, education, personality) VALUES(?,?,?,?,?,?,?,?,?,?)",
	(username, email, image_file, password, state, age, height, gender, education, personality))
	conn.commit()
	
	prefage=random.choice(agepr)
	prefstate=random.choice(stc)
	prefpersonality=random.choice(pepre)
	prefeducation=random.choice(edpre)
	perfheight=random.choice(pehi)
	username=username
		
	c.execute("INSERT INTO Preferences(prefage, prefstate, prefeducation, prefpersonality, perfheight, username) VALUES(?,?,?,?,?,?)",
	(prefage,prefstate,prefeducation,prefpersonality,perfheight,username))
	conn.commit()

for i in range(100):
	inputdata()
c.close()
conn.close()