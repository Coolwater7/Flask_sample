from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=False)
	password = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(120), unique=True)
	emailCheckYn = db.Column(db.String(1), unique=False)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
		self.emailCheckYn = 'N'

	def __repr__(self):
		return '<User %r>' % self.username