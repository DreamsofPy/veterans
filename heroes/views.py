import jinja2
from flask import render_template, flash, url_for, redirect
from flask.ext import wtf
from flask.ext.wtf import validators

import re
import logging

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from heroes import app
@app.route('/')
def hello_world(name=None):
    return render_template("home.html", name=name)

@app.route('/heroes') # welcome page for heros
def heroes(name=None):
    return render_template("heroes.html", name=name)

@app.route('/heroes/<id>')
def hero_id(name=None):
    return render_template("hero_id.html", name=name)

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


# BELOW STUFF MAY NOT BE USED

@app.route('/map')
def map(name=None):
    return render_template("home.html", name=name)

@app.route('/view')
def viewgift(name=None):
    return render_template("home.html", name=name)

@app.route('/add')
def addpost(name=None):
    return render_template("home.html", name=name)

@app.route('/tour')
def tour(name=None):
    return render_template("home.html", name=name)


# DEMO OF THE FLAT-UI KIT

@app.route('/theme')
def show_theme(name=None):
    return render_template("flat-ui-kit.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    """ Renders 404 Error page """
    return render_template('404.html'), 404
