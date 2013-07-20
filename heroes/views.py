import jinja2
from flask import render_template, flash, url_for, redirect
from flask.ext import wtf
from flask.ext.wtf import validators

import re
import logging
import requests
import sendgrid

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView


from instagram import client, subscriptions
from instagram.models import User


#posts = Blueprint('posts', __name__, template_folder='templates')

from heroes import app

CONFIG = {
    'client_id': 'c692be924c234456ad1f6081e28cbea4',
    'client_secret': '28f8d56275a5480f9ba3d7d7d77193c6',
    'redirect_uri': 'http://localhost:5000/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)
reactor = subscriptions.SubscriptionsReactor()

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


@app.route('/heroes/<hero_id>/video', methods=['GET'])
def upload_video(hero_id):
    """
    User logins into instagram... Selects video from their own profile.
    """
    try:
        url = unauthenticated_api.get_authorize_url()
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception, e:
        print e


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

        return ''.join(photos+videos)

#        recent_media, next = api.user_recent_media()
#        photos = []
#        for media in recent_media:
            #photos.append(media)
#            photos.append(media['link'])
#        return ''.join(photos)
    except Exception, e:
        print e



def send_email(subject, plain_text, html):
    """Send grid"""
	
	# make a secure connection to SendGrid
    s = sendgrid.Sendgrid(
		'veteranshack',
		'cbs'+'local'+'1',
		secure=True
	)

	# make a message object
    message = sendgrid.Message(
		("from@veteranshack.com", 'Veterans Hackathon'),
        subject,
        plain_text,
        html,
    )

    # From db pull emails ... Heroes. List of emails.
    q = ['asdf@asdf.com', 'andso@on.com']
    message.add_to(q)

	# use the Web API to send your message
    s.web.send(message)
