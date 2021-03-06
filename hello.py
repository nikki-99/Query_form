
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField,PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
# from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
   
# never hardcode string
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SUBJECT_PREFIX'] = '[Query] '
app.config['MAIL_SENDER'] = 'Admin <nikitadasmsd@gmail.com>'

app.config['ADMIN'] = os.environ.get('ADMIN')

mail=Mail(app)
db = SQLAlchemy(app)
# migrate = Migrate(app,db)


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone_no = db.Column(db.Integer, unique = True, nullable = False)
    subject = db.Column(db.String(120),nullable = False)
    query_msg = db.Column(db.String(120), nullable = False)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.phone_no}','{self.subject}','{self.query_msg}' )"
        


def send_mail(to,subject,template,**kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    mail.send(msg)

class ContactForm(FlaskForm):
    Name = StringField('Name',validators = [DataRequired()])
    email = StringField('Email',validators = [DataRequired()])
    phone_no = StringField('Phone_no',validators = [DataRequired()])
    subject = StringField('Subject',validators = [DataRequired()])
    query_msg = TextAreaField('Query',validators = [DataRequired()])
    
    submit = SubmitField('Submit')

 
@app.route('/',methods =['GET','POST'])
def contact():
   
    form = ContactForm()
    if form.validate_on_submit():
          
        session['Name'] = form.Name.data
    
        form.Name.data = ''
        
        session['email'] = form.email.data     
        form.email.data = ''

        session['phone_no'] = form.phone_no.data
        form.phone_no.data=''
        session['subject'] = form.subject.data
        form.subject.data = ''
        session['query_msg'] = form.query_msg.data
        form.query_msg.data = ''
        user = User.query.filter_by(email = session['email']).first()
        if user is None:
            u = User(username = session['Name'] , email = session['email'], phone_no =session['phone_no'],subject = session['subject'], query_msg = session['query_msg'])
            db.session.add(u)
            db.session.commit()
       
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'], 'New Query Posted', 'mail/new_query',name=session['Name'],email=session['email'],phone_no=session['phone_no'],sub=session['subject'],query_msg=session['query_msg'])
        
        flash('Query has been posted. Soon you will get reply!!')
        return redirect(url_for('contact'))

    return render_template('contact.html',form=form, Name = session.get('Name'),email = session.get('email'),phone_no = session.get('phone_no'),subject = session.get('subject'), query_msg = session.get('query_msg'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500 


