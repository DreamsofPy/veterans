
import jinja2
from flask import render_template, flash, url_for, redirect
from flask.ext import wtf
from flask.ext.wtf import validators

import re
import logging
import sendgrid

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

#posts = Blueprint('posts', __name__, template_folder='templates')

from heroes import app
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
