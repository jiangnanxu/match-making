import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table import *

engine = create_engine('sqlite:///data.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

per = Per("jojo","All","All","All")
session.add(per)

per = Per("dio","Same","EL","LE")
session.add(per)

per = Per("kujo","Same","EL","LE")
session.add(per)

per = Per("josuke","Same","BE","LE")
session.add(per)

per = Per("lily","All","BE","All")
session.add(per)

per = Per("rose","Same","EL","HE")
session.add(per)

per = Per("tara","Same","BE","HE")
session.add(per)

per = Per("Linn","Same","All","HE")
session.add(per)

session.commit()