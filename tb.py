from datetime import datetime
from app import db, login_manager

class results(db.Model):
	id = db.Column(db.Integer, primary_key=true)
	uid = db.Column(db.Integer)
	name = db.String(db.String(60), nullable=False)
	score = db.String(db.sting(60), nullable=False)
	
	def __repr__(self):
        return f"results('{self.uid}','{self.name}','{self.score}')"