from flask import render_template, flash, redirect, request, session, url_for, abort
from app import app, db
from User import User
from flask_mail import Mail, Message as MailMessage

from time import strftime
import base64

mail = Mail(app)

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

@app.route('/login', methods=['GET'])
def loginForm():
  return render_template('login.html')
 
@app.route('/login', methods=['POST'])
def login():
  
  user = db.session.query(User).filter(User.email==request.form['email']).filter(User.password==request.form['password']).first()

  if user:
    
    if user.emailCheckYn == 'N':
      abort(400, {'errorMsg':'Need to validate Email', 'errorDesc':'Check your email'})  
    else:
      session['email'] = user.email
      return redirect(url_for('index'))
  else:
    abort(400, {'errorMsg':'Fail to login', 'errorDesc':'Check Email/Password'})
    # return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route('/signUp', methods=['GET'])
def signUpForm():
  return render_template('signUp.html')

@app.route('/signUp', methods=['POST'])
def signUp():

  print request.form
  user = User(request.form['username'], request.form['password'], request.form['email'])
  user.regAton = strftime("%Y%m%d%H%M%S")

  # db.create_all() # In case user table doesn't exists already. Else remove it.    
  db.session.add(user)
  db.session.commit() # This is needed to write the changes to database

  # checkUrl = "http://localhost:8080/checkEmail?email=" + request.form['email'] +"&key="+base64.encodestring(user.regAton)
  checkUrl = app.config['DOMAIN']+"checkEmail?email=" + request.form['email'] +"&key="+base64.encodestring(user.regAton)

  msg = MailMessage('Hello', recipients = [request.form['email']])
  msg.body = "Test Site Email : " 
  msg.html = "<a href='"+checkUrl+"'>Email Auth</a>"
  mail.send(msg)

  return redirect(url_for('login'))


@app.route('/checkEmail', methods=['GET'])
def checkEmail():
  encAton = request.args['key']
  regAton = base64.decodestring(encAton)

  print request.args['email']

  user = db.session.query(User).filter(User.email==request.args['email']).filter(User.regAton==regAton).first()

  if user:
    user.emailCheckYn='Y'
    db.session.commit()
    return redirect(url_for('login'))
  else:
    abort(400, {'errorMsg':'Fail to authenticate Email', 'errorDesc':'Check your Email again'})

@app.errorhandler(404)
def page_not_found(error):
  return render_template('error.html', errorMsg='Page Not Found!', errorDesc='404 error')

@app.errorhandler(400)
def serverError(error):
  return render_template('error.html', errorMsg=error.description['errorMsg'], errorDesc=error.description['errorDesc'])



@app.route('/db')
def dbCreate():

  db.create_all() # In case user table doesn't exists already. Else remove it.    

  # db.session.add(admin)

  # db.session.commit() # This is needed to write the changes to database

  # print User.query.all()

  # return User.query.filter_by(username='admin').first().email