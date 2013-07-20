from flask import render_template, flash, url_for, redirect, request
import jinja2

from flask.ext import wtf
from flask.ext.wtf import validators
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from heroes import app

import sendgrid
import requests

from instagram import client, subscriptions
from instagram.models import User

#: Database settings
DBUSER = 'root'  # *************
DBPASS = ''  # *************
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

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/heroes') # welcome page for heros
def heroes():
    return render_template("heroes.html")

@app.route('/heroes/<id>')
def hero_id(id):
    return render_template("hero_id.html", id=id)


@app.route('/heroes/all')
def heroes_all(name=None):
    return render_template("heroes_all.html", name=name)

@app.route('/heroes/open') #Curated messages
def curated_messages(name=None):
    return render_template("curated_messages.html", name=name)

@app.route('/supporters')
def supporters(name=None):
    return render_template("supporters.html", name=name)

@app.route('/supporters/message')
def post_message(name=None):
    return render_template("post_message.html", name=name)

def show_theme(name=None):
    return render_template("flat-ui-kit.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    """ Renders 404 Error page """
    return render_template('404.html'), 404

@app.route('/heroes/<hero_id>/video', methods=['GET'])
def upload_video():
    """
    User logins into instagram... Selects video from their own profile.
    """
    try:
        ## this is the connect url
        url = unauthenticated_api.get_authorize_url()
        print '<a href="%s">Connect with Instagram</a>' % url
        return render_template("hero_addvid.html", authurl=url)
    except Exception, e:
        print e

# @app.route('/heroes/<hero_id>/video')
# def choose_video(hero_id, videos):
#     """
#     Select video.
#     """

@app.route('/oauth_callback')
def on_callback():
    code = request.args.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'

        api = client.InstagramAPI(access_token=access_token[0])
        user = api.user()

        data = {
            'access_token': access_token[0],
        }
        url = 'https://api.instagram.com/v1/users/%s/media/recent' % user.id
        r = requests.get(url, params=data)
        r = r.json()

        photos = []
        videos = []
        for media in r.get('data'):
            media_type = media.get('type')
            link = media.get('link')
            if media_type == 'video':
                videos.append(link)
            else:
                photos.append(link)

        return redirect(url_for('choose_video', ))

    except Exception, e:
        print e

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
