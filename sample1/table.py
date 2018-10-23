from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

class User(Base):
	
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	gender = Column(String)
	age = Column(Integer)
	address = Column(String)
	income = Column(Integer)
	
	def __init__(self, name, gender, age, address, income):
		
		self.name = name
		self.gender = gender
		self.age = age
		self.address = address
		self.income = income

class Per(Base) : 
	
	__tablename__ = "pers"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	peradd = Column(String)
	perage = Column(String)
	perin = Column(String)
	
	def __init__(self, name, peradd, perage, perin):
		
		self.name = name
		self.peradd = peradd
		self.perage = perage
		self.perin = perin

Base.metadata.create_all(engine)