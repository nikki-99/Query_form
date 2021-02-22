# from flask import Flask, render_template, redirect, url_for, flash, session
# from flask_wtf import FlaskForm
# from wtforms import StringField,TextAreaField, SubmitField,PasswordField
# from wtforms.validators import DataRequired

# from flask_mail import Mail, Message



# app = Flask(__name__)
   

# app.config['SECRET_KEY'] = 'hard to guess'

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'nikitadasmsd@gmail.com'
# app.config['MAIL_PASSWORD'] = 'trex1999@'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail=Mail(app)



# class ContactForm(FlaskForm):
#     Name = StringField('Name',validators = [DataRequired()])
#     email = StringField('Email',validators = [DataRequired()])
#     phone_no = StringField('Phone_no',validators = [DataRequired()])
#     subject = StringField('Subject',validators = [DataRequired()])
#     query = TextAreaField('Query',validators = [DataRequired()])
    
#     submit = SubmitField('Submit')


# @app.route('/',methods =['GET','POST'])
# def contact():
   
#     form = ContactForm()
#     if form.validate_on_submit():
#         session['Name'] = form.Name.data
#         form.Name.data = ''
#         session['email'] = form.email.data
#         form.email.data = ''

#         session['phone_no'] = form.phone_no.data
#         form.phone_no.data=''
#         session['subject'] = form.subject.data
#         form.subject.data = ''
#         session['query'] = form.query.data
#         form.query.data = ''
     
        
#         message = Message(session.get('subject'),sender="nikitadasmsd@gmail.com",recipients=[session.get('email')])
#         message.body = "NAME = " + session.get('Name') + '\n\n' + "PHONE NO = " + session.get('phone_no')+'\n\n' + "QUERY = " + session.get('query')
        
#         mail.send(message)
        
#         flash('Thanks for submission ..Have a nice day!!.Your mail has been sent')
#         return redirect(url_for('contact'))



#     return render_template('contact.html',form=form, Name = session.get('Name'),email = session.get('email'),phone_no = session.get('phone_no'),subject = session.get('subject'), query = session.get('query'))


   
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'),404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'),500 







# **************************************************



from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField,PasswordField
from wtforms.validators import DataRequired

from flask_mail import Mail, Message
import os


app = Flask(__name__)
   

app.config['SECRET_KEY'] = 'hard to guess'

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
    query = TextAreaField('Query',validators = [DataRequired()])
    
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
        session['query'] = form.query.data
        form.query.data = ''
        # flash('Thanks for submission ....Have a nice day!!')
        # return redirect(url_for('contact'))
        
        # message = Message(session.get('subject'),sender="nikitadasmsd@gmail.com",recipients=[session.get('email')])
        # message.body = "NAME = " + session.get('Name') + '\n\n' + "PHONE NO = " + session.get('phone_no')+'\n\n' + "QUERY = " + session.get('query')
        
        # mail.send(message)
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'], 'New Query Posted', 'mail/new_query',name=session['Name'],email=session['email'],phone_no=session['phone_no'],sub=session['subject'],query=session['query'])
        # flash("Mail sent")
        flash('Thanks for submission ..Have a nice day!!.Your mail has been sent')
        return redirect(url_for('contact'))







    return render_template('contact.html',form=form, Name = session.get('Name'),email = session.get('email'),phone_no = session.get('phone_no'),subject = session.get('subject'), query = session.get('query'))


   
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500 