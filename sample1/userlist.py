import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table import *

engine = create_engine('sqlite:///data.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

user = User("jojo","male",25,"Victoria",20000)
session.add(user)

user = User("dio","male",25,"Victoria",15000)
session.add(user)

user = User("kujo","male",19,"Queensland",30000)
session.add(user)

user = User("josuke","male",22,"New South wales",2000)
session.add(user)

user = User("lily","female",23,"Victoria",60000)
session.add(user)

user = User("rose","female",24,"Victoria",5000)
session.add(user)

user = User("tara","female",21,"Queensland",33000)
session.add(user)

user = User("Linn","female",18,"Victoria",14500)
session.add(user)

session.commit()
