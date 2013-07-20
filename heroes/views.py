from flask import render_template, flash, url_for, redirect, request
from flask.ext import wtf
from flask.ext.wtf import validators
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from heroes import app

import sendgrid

#: Database settings
DBUSER = 'neo'  # *************
DBPASS = 'mysql'  # *************
DBHOST = 'localhost'  # host ip or localhost
DBNAME = 'veterans'  # database name
DB = 'mysql'  # sqlite / mysql/ postgresql

#: database configuration
SQLALCHEMY_DATABASE_URI = DB + '://' + DBUSER + ':' + DBPASS + '@' + \
                          DBHOST + '/' + DBNAME
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

SQLALCHEMY_ECHO = True
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
DEBUG = True

db = SQLAlchemy(app)

# MODELS

class Heroes(db.Model):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)
    hometown = Column(String(30), unique=False)
    branch_of_service = Column(String(30), unique=False)
    rank = Column(String(30), unique=False)
    story = Column(Text(350), unique=False)
    photo = Column(Text(100), unique=False)
    email = Column(String(30), unique=True)

class Supporters(db.Model):
    __tablename__ = 'supporters'
    id = Column(Integer, primary_key=True)
    fb_email = Column(String(30), unique=False)
    fbuid = Column(Integer, primary_key=True)
    fb_name = Column(String(30), unique=False)
    profile_pic = Column(Text(100), unique=False)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    supporter_id = Column(Integer, ForeignKey('supporters.id'))
    text_message = Column(Text(120), unique=False)
    instagram_url = Column(Text(200), unique=False)

#posts = Blueprint('posts', __name__, template_folder='templates')



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/heroes/open')
def curated_messages():
    return render_template("curated_messages.html")

@app.route('/theme')
def show_theme():
    return render_template("theme.html")

@app.errorhandler(404)
def page_not_found(e):
    """ Renders 404 Error page """
    return render_template('404.html'), 404

@app.route('/blast', methods=['POST'])
def send_email():
    """Send grid"""

	# make a secure connection to SendGrid
    s = sendgrid.Sendgrid(
		'veteranshack',
		'cbs'+'local'+'1',
		secure=True
	)

	# make a message object
    message = sendgrid.Message(
		"from@mydomain.com",
		"message subject",
		"plaintext message body",
	    "HTML message body"
    )

	# add a recipient
    message.add_to(
		"someone@example.com",
		"John Doe"
	)

	# use the Web API to send your message
    s.web.send(message)
