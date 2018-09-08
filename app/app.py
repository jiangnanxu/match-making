from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
#from passlib.hash import sha256_crypt

app = Flask(__name__)

# Confi MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'S3563105'
app.config['MYSQL_DB'] = 'Social'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

#Python Registration
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    city = StringField('City', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.date
        email = form.email.date
        city = form.city.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, city, password) VALUES(%s, %s, %s, %s)", (name, email, city, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
        
        return render_template('register.html',)
    return render_template('register.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                          title='Sign In',
                          form=form)

if __name__=='__main__':
    app.run(debug=True)