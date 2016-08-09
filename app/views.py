from flask import render_template, flash, redirect, request
from app import app, db
from forms import LoginForm
from User import User
# from Mail import mail, MailMessage
from flask_mail import Mail, Message as MailMessage

mail = Mail(app)

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Miguel'}  # fake user
	posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
	return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
    return redirect('/index')
  return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/signUp', methods=['GET'])
def signUpForm():
  return render_template('signUp.html')

@app.route('/signUp', methods=['POST'])
def signUp():

  print request.data
  user = User(request.form['username'], request.form['password'], request.form['email'])
  # db.create_all() # In case user table doesn't exists already. Else remove it.    
  db.session.add(user)
  db.session.commit() # This is needed to write the changes to database

  msg = MailMessage('Hello', recipients = [request.form['email']])
  msg.body = "Email Auth : <a href=''>Auth</a>"
  mail.send(msg)
  return "Sent"



@app.route('/db')
def dbcheck():
  admin = User('admin', 'admin@example.com')

  # db.create_all() # In case user table doesn't exists already. Else remove it.    

  # db.session.add(admin)

  # db.session.commit() # This is needed to write the changes to database

  print User.query.all()

  return User.query.filter_by(username='admin').first().email