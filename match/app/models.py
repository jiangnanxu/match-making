from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(20), unique=True,nullable=False)
     email = db.Column(db.String(120), unique=True,nullable=False)
     image_file = db.Column(db.String(20),nullable=False, default='static/profile_pics/default.jpg')
     password = db.Column(db.String(60), nullable=False)
     state = db.Column(db.String(60))
     age = db.Column(db.Integer)
     gender = db.Column(db.String(8))
     education = db.Column(db.String(60))
     personality = db.Column(db.String(60))
     posts = db.relationship('Post', backref='author', lazy=True)
     # Preference db relationship   
     preferences = db.relationship('Preferences', backref='pref', lazy=True)

     def is_active(self):
        return True
     def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class results(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer)
	name = db.Column(db.String(60))
	score = db.Column(db.String(60))
	
	def __repr__(self):
            return f"results('{self.uid}','{self.name}','{self.score}')"

    # Preference db 
class Preferences(db.Model):
    preferencesid = db.Column(db.Integer, primary_key=True)
    prefage = db.Column(db.String(60))
    prefstate = db.Column(db.String(60))
    prefpersonality = db.Column(db.String(60))
    prefeducation = db.Column(db.String(60))
    
    username = db.Column(db.String, db.ForeignKey('user.username'))
    
    def is_active(self):
        return True
    def __repr__(self):
        return f"Preferences('{self.prefage}','{self.prefstate}','{self.prefpersonality}','{self.prefeducation}')"