from flask import Flask
from flask_mail import Mail, Message as MailMessage

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ms4096@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'ms4096@gmail.com'

mail = Mail(app)
